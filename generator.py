import os
import time
import random
from datetime import datetime

import psycopg2
from dotenv import load_dotenv
from faker import Faker

load_dotenv()
fake = Faker()

CITIES = ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Peshawar", "Quetta", "Multan", "Faisalabad"]
CATEGORIES = ["Food", "Bills", "Shopping", "Mobile Load", "Transport", "Education"]
TXN_TYPES = ["Send Money", "Bill Payment", "Mobile Load", "Cash Out"]
DEVICES = ["Mobile App", "USSD", "Web"]
USERS = [f"U{i:04d}" for i in range(1, 501)]


def make_transaction():
    is_fraud = random.random() < 0.03

    if is_fraud:
        amount = round(random.uniform(40000, 200000), 2)
        txn_type = random.choice(["Send Money", "Cash Out"])
        device = random.choice(["USSD", "Web"])
    else:
        amount = round(random.uniform(50, 15000), 2)
        txn_type = random.choice(TXN_TYPES)
        device = random.choice(DEVICES)

    return (
        fake.uuid4(),
        random.choice(USERS),
        random.choice(CITIES),
        random.choice(CATEGORIES),
        txn_type,
        amount,
        device,
        datetime.now(),
        is_fraud,
    )


conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

try:
    while True:
        t = make_transaction()
        cur.execute(
            """INSERT INTO raw.transactions
               (transaction_id, user_id, city, merchant_category,
                txn_type, amount, device_type, txn_time, is_fraud)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            t,
        )
        conn.commit()
        print(t[0][:8], t[2], t[5], "FRAUD" if t[8] else "ok")
        time.sleep(1)
except KeyboardInterrupt:
    print("Generator band kar diya.")
finally:
    conn.close()
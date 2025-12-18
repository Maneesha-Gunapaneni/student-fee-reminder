from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime

app = Flask(__name__)
CORS(app)

CSV_PATH = 'students.csv'



# ---------- STEP 1: Create CSV file if not exists ----------
def create_csv():
    try:
        df = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        data = {
            'StudentID': [1, 2, 3, 4],
            'Name': ['John', 'Mary', 'Alex', 'Sophia'],
            'ParentContact': ['9876543210', '8765432109', '7654321098', '6543210987'],
            'Term1Fee': [5000, 5000, 5000, 5000],
            'Term2Fee': [5000, 5000, 5000, 5000],
            'PaidTerm1': [5000, 3000, 5000, 2000],
            'PaidTerm2': [5000, 0, 2000, 0],
            'SystemDate': [datetime.now().strftime('%Y-%m-%d')] * 4,
            'DueDate': ['2025-11-10', '2025-11-10', '2025-11-10', '2025-11-10']
        }
        df = pd.DataFrame(data)
        df.to_csv(CSV_PATH, index=False)
        print("CSV file created successfully.")

create_csv()




# ---------- STEP 2: Calculate pending fees ----------
def calculate_pending_fees():
    df = pd.read_csv(CSV_PATH)
    df['PendingTerm1'] = df['Term1Fee'] - df['PaidTerm1']
    df['PendingTerm2'] = df['Term2Fee'] - df['PaidTerm2']
    df['TotalPending'] = df['PendingTerm1'] + df['PendingTerm2']

    pending_df = df[df['TotalPending'] > 0]
    return pending_df


# ---------- STEP 3: Flask API ----------
@app.route('/pending-fees', methods=['GET'])
def pending_fees():
    pending_df = calculate_pending_fees()
    pending_students = pending_df.to_dict(orient='records')
    return jsonify(pending_students)


# ---------- STEP 4: Simulate sending messages ----------
@app.route('/send-messages', methods=['GET'])
def send_messages():
    pending_df = calculate_pending_fees()
    messages = []

    for _, row in pending_df.iterrows():
        msg = (f"Reminder: {row['Name']}'s pending fee is ₹{row['TotalPending']} "
               f"due by {row['DueDate']}. Please pay soon.")
        messages.append({'ParentContact': row['ParentContact'], 'Message': msg})
        print(f"📩 Message sent to {row['ParentContact']}: {msg}")

    return jsonify({'status': 'Messages sent', 'messages': messages})


if __name__ == '__main__':
    app.run(debug=True)



















    

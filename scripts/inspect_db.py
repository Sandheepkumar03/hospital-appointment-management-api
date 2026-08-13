import sqlite3
import json

con = sqlite3.connect('hospital.db')
cur = con.cursor()

print('Doctors:')
for row in cur.execute('SELECT id, name, specialization FROM doctors'):
    print(json.dumps(row))

print('\nPatients:')
for row in cur.execute('SELECT id, name, email, phone FROM patients'):
    print(json.dumps(row))

print('\nAppointments:')
for row in cur.execute('SELECT id, patient_id, doctor_id, appointment_start, appointment_end FROM appointments'):
    print(json.dumps(row))

con.close()

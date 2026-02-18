import gspread
from oauth2client.service_account import ServiceAccountCredentials
import mysql.connector
import time
import datetime
import os

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/home/crm-api/your_credentials.json", scope)
client = gspread.authorize(creds)
sheet_orders = client.open_by_key("1nwmKReLDFFtPuGVVUygQrZKXQ5wC2BbGhf4K6EH901k").sheet1
sheet_invoices = client.open_by_key("1qVFFf9f5imgRUqMNV14lnBjlPgB36WJqakEOjAu6a5I").sheet1

# MySQL setup
conn = mysql.connector.connect(
    host="localhost",
    user="marketplace_software_user",
    password="ChangeMe_Strong1!",
    database="MarketPlaceSoftwareDB"
)
cursor = conn.cursor()

def safe_str(field, max_len):
    try:
        return str(field).strip()[:max_len]
    except:
        return ""

def safe_text(field, max_len=None):
    try:
        text = str(field).strip()
        return text[:max_len] if max_len else text
    except:
        return ""

def safe_date(field):
    try:
        return datetime.datetime.strptime(field, "%d/%m/%Y").date()
    except:
        return None

def insert_row(row, source):
    try:
        cursor.execute("""
            INSERT INTO orders (
                order_date, order_number, department, employee, payment_method,
                customer_name, phone_number, personal_id, product_name, quantity,
                revenue, contribution, bank, city, branch, location_details,
                item_carrier, delivery_type, planned_delivery_time, order_ready_status,
                item_collection_note, location_movement, order_status_1, tracking_code,
                delivery_status_2, delivery_date_fx, days_diff_fx, order_deadline_fx,
                standard_deadline, status_update, failed_delivery_comment, resend_date,
                comment_1, issue_date, status, source_sheet
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s, %s, %s, %s, %s, %s)
        """, (
            row.get('order_date'), row.get('order_number'), row.get('department'), row.get('employee'),
            row.get('payment_method'), row.get('customer_name'), row.get('phone_number'), row.get('personal_id'),
            row.get('product_name'), row.get('quantity'), row.get('revenue'), row.get('contribution'),
            row.get('bank'), row.get('city'), row.get('branch'), row.get('location_details'),
            row.get('item_carrier'), row.get('delivery_type'), row.get('planned_delivery_time'),
            row.get('order_ready_status'), row.get('item_collection_note'), row.get('location_movement'),
            row.get('order_status_1'), row.get('tracking_code'), row.get('delivery_status_2'),
            row.get('delivery_date_fx'), row.get('days_diff_fx'), row.get('order_deadline_fx'),
            row.get('standard_deadline'), row.get('status_update'), row.get('failed_delivery_comment'),
            row.get('resend_date'), row.get('comment_1'), row.get('issue_date'),
            row.get('status'), source
        ))
        return True
    except Exception as e:
        print(f"❌ Error inserting row: {e} | Row preview: {row}")
        return False

def refresh_data():
    inserted = 0
    skipped = 0
    cursor.execute("DELETE FROM orders")

    # Sheet 1: Orders
    headers_orders = [
        'თარიღი', 'ორდერ #', 'დეპარტამენტი', 'თანამშრომელი',
        'გადახდის მეთოდი - For E-Commerce', 'მომხმარებელი/კომპანია',
        'ტელ. ნომერი', 'პირადი ნომერი/ს.კ', 'ნომენკლატურა', 'რაოდ-ბა',
        'შემოსავალი ₾', 'თანამონაწილოება - For E-Commerce',
        'ბანკი For E-Commerce', 'ქალაქი/სოფელი',
        'მისამართი/ფილიალი/საწყობი - ლოკაცია...',
        'ნივთის გამტანი - აღნიშნული გრაფა...', 'მიწოდების ტიპი',
        'დაგეგმილი მიწოდების საათი', 'გამზადებულია შეკვეთა',
        'ნივთის მოგროვება - ეს სვეტი...',
        'ლოკაცია (მოსვლა-წასვლის)...',
        'შეკვეთის სტატუსი #1',
        'ALL Tracking Code - ივსება TNT, Quickshipper & Georgian Post-ის გზავნილის კოდები',
        'ორდერის მიწოდების სტატუსი #2',
        'გაგზავნა/ჩაბარების თარიღი FX',
        'Days Diff FX',
        'Order Deadline Untill Delivery FX',
        'სტანდარტული მიწოდების Deadline',
        'Status Update - ინიშნება საწყობიდან...',
        'ვერ ჩაბარების კომენტარი',
        'განმეორებითი გაგზავნის თარიღი'
    ]

    try:
        data_orders = sheet_orders.get_all_records(expected_headers=headers_orders)
        for row in data_orders:
            mapped = {
                'order_date': safe_date(row['თარიღი']),
                'order_number': safe_str(row['ორდერ #'], 30),
                'department': safe_str(row['დეპარტამენტი'], 100),
                'employee': safe_str(row['თანამშრომელი'], 100),
                'payment_method': safe_str(row['გადახდის მეთოდი - For E-Commerce'], 100),
                'customer_name': safe_str(row['მომხმარებელი/კომპანია'], 150),
                'phone_number': safe_str(row['ტელ. ნომერი'], 50),
                'personal_id': safe_str(row['პირადი ნომერი/ს.კ'], 30),
                'product_name': safe_str(row['ნომენკლატურა'], 255),
                'quantity': safe_str(row['რაოდ-ბა'], 20),
                'revenue': safe_str(row['შემოსავალი ₾'], 50),
                'contribution': safe_str(row['თანამონაწილოება - For E-Commerce'], 100),
                'bank': safe_str(row['ბანკი For E-Commerce'], 100),
                'city': safe_str(row['ქალაქი/სოფელი'], 100),
                'location_details': safe_text(row[headers_orders[14]]),
                'item_carrier': safe_str(row[headers_orders[15]], 100),
                'delivery_type': safe_str(row['მიწოდების ტიპი'], 100),
                'planned_delivery_time': safe_str(row['დაგეგმილი მიწოდების საათი'], 50),
                'order_ready_status': safe_str(row['გამზადებულია შეკვეთა'], 100),
                'item_collection_note': safe_text(row['ნივთის მოგროვება - ეს სვეტი...']),
                'location_movement': safe_text(row['ლოკაცია (მოსვლა-წასვლის)...']),
                'order_status_1': safe_str(row['შეკვეთის სტატუსი #1'], 100),
                'tracking_code': safe_text(row['ALL Tracking Code - ივსება TNT, Quickshipper & Georgian Post-ის გზავნილის კოდები']),
                'delivery_status_2': safe_str(row['ორდერის მიწოდების სტატუსი #2'], 100),
                'delivery_date_fx': safe_date(row['გაგზავნა/ჩაბარების თარიღი FX']),
                'days_diff_fx': safe_str(row['Days Diff FX'], 20),
                'order_deadline_fx': safe_str(row['Order Deadline Untill Delivery FX'], 50),
                'standard_deadline': safe_date(row['სტანდარტული მიწოდების Deadline']),
                'status_update': safe_text(row['Status Update - ინიშნება საწყობიდან...']),
                'failed_delivery_comment': safe_text(row['ვერ ჩაბარების კომენტარი']),
                'resend_date': safe_date(row['განმეორებითი გაგზავნის თარიღი']),
                'source_sheet': 'orders'
            }
            if insert_row(mapped, 'orders'):
                inserted += 1
            else:
                skipped += 1
    except Exception as e:
        print(f"❌ Error reading orders sheet: {e}")

# Sheet 2: Invoices
    headers_invoices = [
        'თარიღი', 'ინვოისი #', 'მომხმარებელი', 'პირადი ნომერი',
        'ფილიალი', 'პროდუქტი', 'კომენტარი 1',
        'გაცემის თარიღი', 'სტატუსი'
    ]

    try:
        data_invoices = sheet_invoices.get_all_records(expected_headers=headers_invoices)
        for row in data_invoices:
            mapped = {
                'order_date': safe_date(row['თარიღი']),
                'order_number': safe_str(row['ინვოისი #'], 30),
                'customer_name': safe_str(row['მომხმარებელი'], 150),
                'personal_id': safe_str(row['პირადი ნომერი'], 30),
                'branch': safe_str(row['ფილიალი'], 100),
                'product_name': safe_str(row['პროდუქტი'], 255),
                'comment_1': safe_text(row['კომენტარი 1']),
                'issue_date': safe_date(row['გაცემის თარიღი']),
                'status': safe_str(row['სტატუსი'], 100),
                'source_sheet': 'invoices'
            }
            if insert_row(mapped, 'invoices'):
                inserted += 1
            else:
                skipped += 1
    except Exception as e:
        print(f"❌ Error reading invoices sheet: {e}")

    conn.commit()
    print(f"✅ Data refreshed at {datetime.datetime.now().strftime('%H:%M:%S')} | Inserted: {inserted} rows | Skipped: {skipped} rows")

if __name__ == "__main__":
    run_once = os.getenv("RUN_ONCE") == "1"
    if run_once:
        refresh_data()
    else:
        # Refresh every 5 minutes
        while True:
            refresh_data()
            time.sleep(300)
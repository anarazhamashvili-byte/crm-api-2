# MarketPlaceSoftwareAPI — გამოყენების ინსტრუქცია (ქართულად)

## სწრაფი მიმოხილვა
ეს არის Flask-ზე დაფუძნებული API, რომელიც:
- კითხულობს CRM მონაცემებს Google Sheets-იდან და წერს MySQL-ში
- აბრუნებს შეკვეთებს ფილტრით


## ავტორიზაცია
endpoint მოითხოვს API key-ს query პარამეტრში:

- `api_key=<API_KEY>`

## სერვერის მისამართი და API Key
- `SERVER_IP`: `165.22.66.5`
- `API_KEY`: `a3f9b8c2d1e44f7a9c0d5e6f8a7b2c1d9e0f3a4b5c6d7e8f9a0b1c2d3e4f5a6b`

## Endpoint-ები

### 1) შეკვეთების მიღება
```
GET /api/orders?api_key=<API_KEY>&order_number=<ORDER_NUMBER>
```

შეგიძლიათ ფილტრი გამოიყენოთ შემდეგი პარამეტრებით:
- `order_number`
- `phone_number`
- `personal_id`

მაგალითი:
```
curl -sS "http://<SERVER_IP>/ordersdata/api/orders?api_key=<API_KEY>&order_number=3710180"
```

## სვეტების შესაბამისობა (ქართულიდან ინგლისურზე)

ქვემოთ მოცემულია Google Sheet-ის ქართული სვეტები და მათი შესაბამისი ველები ბაზაში/JSON-ში:

- `თარიღი` → `order_date`
- `ორდერ #` → `order_number`
- `დეპარტამენტი` → `department`
- `თანამშრომელი` → `employee`
- `გადახდის მეთოდი - For E-Commerce` → `payment_method`
- `მომხმარებელი/კომპანია` → `customer_name`
- `ტელ. ნომერი` → `phone_number`
- `პირადი ნომერი/ს.კ` → `personal_id`
- `ნომენკლატურა` → `product_name`
- `რაოდ-ბა` → `quantity`
- ` შემოსავალი ₾` → `revenue`
- `თანამონაწილოება - For E-Commerce` → `contribution`
- `ბანკი For E-Commerce` → `bank`
- `ქალაქი/სოფელი` → `city`
- `მისამართი/ფილიალი/საწყობი - ლოკაცია თუ საიდან ხდება ნივთის გაცემა ან სად ხდება ნივთის მიტანა. სწრაფი მიწოდების ის შემთხვევები როდესაც ნივთის უნდა გაიგზავნოს ფილიალიდან, მისამართთან ერთად აუცილებელია მიეთითოს ფილიალი თუ საიდან ხდება სწრაფი  მიწოდების შესრულება` → `location_details`
- `ნივთის გამტანი - აღნიშნული გრაფა ივსება თუ სხვა პიროვნებას გააქვს/იბარებს ნივთს` → `item_carrier`
- `მიწოდების ტიპი` → `delivery_type`
- `დაგეგმილი მიწოდების საათი` → `planned_delivery_time`
- `გამზადებულია შეკვეთა` → `order_ready_status`
- `ნივთის მოგროვება - ეს სვეტი ივსება თუ ნივთი ადგილზე არ არის (საწყობი/ფილიალი)` → `item_collection_note`
- `"ლოკაცია (მოსვლა-წასვლის) - ეს სვეტი ივსები ნივთების განაწილება/გამონაწილებისას"` → `location_movement`
- `შეკვეთის სტატუსი #1` → `order_status_1`
- `ALL Tracking Code - ივსება TNT, Quickshipper  & Georgian Post-ის გზავნილის კოდები` → `tracking_code`
- ` ორდერის მიწოდების სტატუსი #2` → `delivery_status_2`
- `გაგზავნა/ჩაბარების თარიღი FX` → `delivery_date_fx`
- `Days Diff FX` → `days_diff_fx`
- `Order Deadline Untill Delivery FX` → `order_deadline_fx`
- `სტანდარტული მიწოდების Deadline` → `standard_deadline`
- `Status Update - ინიშნება საწყობიდან გატანის შემთხვევაში ან ნივთის ვერ ჩაბარება/მობრუნების შემთხვევაში` → `status_update`
- `ვერ ჩაბარების კომენტარი` → `failed_delivery_comment`
- `განმეორებითი გაგზავნის თარიღი` → `resend_date`
- `კომენტარი Feel Free :)` → `comment_1`
- `გაცემის თარიღი` → `issue_date` *(Invoices sheet)*
- `სტატუსი` → `status` *(Invoices sheet)*

## ტიპური შეცდომები

**401** — არასწორი `api_key`  
**400** — არ არის გადმოცემული ფილტრი (`order_number`, `phone_number`, `personal_id`)  
**500** — სერვერის შეცდომა ან ბაზასთან დაკავშირების პრობლემა


data = []
with open("/home/zaki/Downloads/spark/bin/Ashesh/orders_demo_data.csv", "r") as file:
    headers = file.readline().strip().split(",") 
    for line in file:
        values = line.strip().split(",")
        if len(values) == len(headers):
            row = dict(zip(headers, values))
            row["amount"] = float(row["amount"])
            data.append(row)
categories = []
for row in data:
    category = row["product_category"]
    if category not in categories:
        categories.append(category)
results = []
for category in categories:
    count = 0
    total = 0.0
    for row in data:
        if row["product_category"] == category:
            count += 1
            total += row["amount"]
    results.append((category, count, total))
results.sort(key=lambda x: x[2])
print(f"{'Category':<15} {'Total Orders':<15} {'Total Amount Paid'}")
print("-" * 45)
for cat, count, total in results:
    print(f"{cat:<15} {count:<15} {total:.2f}")
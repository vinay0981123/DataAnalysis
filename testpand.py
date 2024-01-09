from datetime import datetime

# Get the current date
current_date = datetime.now()

# Format the date as "YYYY-MMdd"
formatted_date = current_date.strftime("%m-%d")

print(formatted_date)
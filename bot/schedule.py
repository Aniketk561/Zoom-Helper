import csv

print("")
print("CREATING SCHEDULE FILE ZOOM: ENTER MEETING DETAILS")
print("")

with open('zoom.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    choice = 'y'

    while choice == 'y':
        name = input("Enter name of meeting/class: ")
        day = input("Enter day of meeting (Monday/Tuesday,etc): ")
        time = input("Enter time of meeting(24 hour like 23:59): ")
        mid = input("Enter zoom meeting ID: ")
        mpass = input("Enter meeting password: ")
        writer.writerow([name, day, time, mid.replace(" ", ""), mpass])

        choice = input("Want to add more meetings ? (y/n)")

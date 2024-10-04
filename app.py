from flask import Flask,render_template,url_for,request
from dataset import mobile_data

app = Flask(__name__)

# Find the closest match value
def find_closest(value, options):
    min_diff = abs(value - options[0])
    for x in range(1, len(options)):
        temp = abs(value - options[x])
        if min_diff > temp:
            min_diff = temp

    closest_match = []
    for x in options:
        if min_diff == abs(value - x):
            closest_match.append(x)

    return closest_match

# Function to suggest a phone based on the nearest specifications
def choise_phone(ram, storage, camera, lower_price_range, upper_price_range, mobile_phones):
    # Extract only the first camera value from the input (before the +)
    camera_value = float(camera.split('+')[0].lower().replace("mp", "").strip())
    
    # Remove 'GB' and handle ram and storage
    ram_value = int(ram.replace("GB", "").strip())
    storage_value = int(storage.replace("GB", "").strip())

    # Filter phones by price range
    phones_in_price_range = [
        phone for phone in mobile_phones
        if lower_price_range <= int(phone[7].replace('₹', '').replace(',', '')) <= upper_price_range
    ]

    # Extract the specifications from the filtered phones
    aval_ram = [float(phone[3].replace("GB", "")) for phone in phones_in_price_range]
    aval_camera = [float(phone[5].split("MP")[0].strip()) for phone in phones_in_price_range]  # Use only the first camera spec
    aval_storage = [float(phone[2].replace("GB", "")) for phone in phones_in_price_range]

    # Get the closest values for each specification
    closest_match_ram = find_closest(ram_value, aval_ram)
    closest_match_camera = find_closest(camera_value, aval_camera)  # Use only the first camera value
    closest_match_storage = find_closest(storage_value, aval_storage)

    # Find and return the matching phone based on the closest specs
    for phone in phones_in_price_range:
        phone_ram = int(phone[3].replace("GB", "").strip())
        phone_camera = float(phone[5].split("MP")[0].strip())  # Consider only the first camera value
        phone_storage = int(phone[2].replace("GB", "").strip())

        if (phone_ram in closest_match_ram and
            phone_camera in closest_match_camera and
            phone_storage in closest_match_storage):
            return f"Suggested phone: {phone[0]} {phone[1]} with specification RAM: {phone[3]}  Storage: {phone[2]}  Camera: {phone[5]}  Price: {phone[7]}"

    return "No phone found matching your specifications."





@app.route('/',methods = ['GET','POST'])

def home():
        if request.method == 'POST':
            ram = request.form['ram']
            storage =request.form['storage']
            camera = request.form['camera']
            lower_price_range = int(request.form['lower_price_range'])
            higher_price_range = int(request.form['higher_price_range'])
            suggested_phone = choise_phone(ram, storage, camera, lower_price_range, higher_price_range,mobile_data)
            return render_template('home.html', suggestion=suggested_phone)


        return render_template('home.html', suggestion=None)
        














if __name__ =='__main__':
    app.run(debug=True)
    

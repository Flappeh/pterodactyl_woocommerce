#!/usr/bin/python3 
from dotenv import load_dotenv
from modules import (
    emails as mail, 
    wordpress as wp,
    renewal,
    panel)
import json, os, sys, requests, random, string

load_dotenv(dotenv_path='.env')

details ={'id': 521, 'parent_id': 0, 'status': 'processing', 'currency': 'EUR', 'version': '7.5.1', 'prices_include_tax': False, 'date_created': '2023-03-27T18:30:57', 'date_modified': '2023-03-27T18:31:01', 'discount_total': '0.00', 'discount_tax': '0.00', 'shipping_total': '0.00', 'shipping_tax': '0.00', 'cart_tax': '0.00', 'total': '44.50', 'total_tax': '0.00', 'customer_id': 2, 'order_key': 'wc_order_QkkMyZ1HpfD6x', 'billing': {'first_name': 'dsfg', 'last_name': 'sdfg', 'company': '', 'address_1': 'testd', 'address_2': '', 'city': 'etst', 'state': 'EC-B', 'postcode': 'ASET', 'country': 'EC', 'email': 'akunbuatgta@gmail.com', 'phone': '9819819811'}, 'shipping': {'first_name': '', 'last_name': '', 'company': '', 'address_1': '', 'address_2': '', 'city': '', 'state': '', 'postcode': '', 'country': '', 'phone': ''}, 'payment_method': 'woocommerce_payments', 'payment_method_title': 'Visa credit card', 'transaction_id': 'pi_3MqJslFfxzqFusuN1Iqngyx3', 'customer_ip_address': '112.78.153.62', 'customer_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', 'created_via': 'checkout', 'customer_note': '', 'date_completed': None, 'date_paid': '2023-03-27T18:31:01', 'cart_hash': '5002d6a44ea87a14f5558fc95b736cba', 'number': '521', 'meta_data': [{'id': 6302, 'key': 'is_vat_exempt', 'value': 'no'}, {'id': 6303, 'key': '_payment_method_id', 'value': 'pm_1MqCLVFfxzqFusuNuGmicQfv'}, {'id': 6304, 'key': '_stripe_customer_id', 'value': 'cus_NaSYdH2SIonifE'}, {'id': 6306, 'key': '_wcpay_mode', 'value': 'test'}, {'id': 6307, 'key': '_intent_id', 'value': 'pi_3MqJslFfxzqFusuN1Iqngyx3'}, {'id': 6308, 'key': '_charge_id', 'value': 'ch_3MqJslFfxzqFusuN1inFo7PR'}, {'id': 6309, 'key': '_intention_status', 'value': 'succeeded'}, {'id': 6310, 'key': '_wcpay_intent_currency', 'value': 'eur'}, {'id': 6314, 'key': '_new_order_tracking_complete', 'value': 'yes'}], 'line_items': [{'id': 8, 'name': 'Galaxy Membership', 'product_id': 214, 'variation_id': 0, 'quantity': 2, 'tax_class': '', 'subtotal': '40.00', 'subtotal_tax': '0.00', 'total': '40.00', 'total_tax': '0.00', 'taxes': [], 'meta_data': [], 'sku': '', 'price': 20, 'image': {'id': '', 'src': ''}, 'parent_name': None}, {'id': 9, 'name': 'Standalone Minecraft Server', 'product_id': 267, 'variation_id': 437, 'quantity': 1, 'tax_class': '', 'subtotal': '4.50', 'subtotal_tax': '0.00', 'total': '4.50', 'total_tax': '0.00', 'taxes': [], 'meta_data': [{'id': 115, 'key': 'ram-gb', 'value': '3', 'display_key': 'RAM (GB)', 'display_value': '3'}, {'id': 116, 'key': 'thread-count', 'value': '4', 'display_key': 'Thread Count', 'display_value': '4'}], 'sku': '', 'price': 4.5, 'image': {'id': 128, 'src': 'https://i0.wp.com/infinity-projects.de/wp-content/uploads/2023/03/minecraft.jpg?fit=1440%2C810&ssl=1'}, 'parent_name': 'Standalone Minecraft Server'}], 'tax_lines': [], 'shipping_lines': [], 'fee_lines': [], 'coupon_lines': [], 'refunds': [], 'payment_url': 'https://infinity-projects.de/checkout-2/order-pay/521/?pay_for_order=true&key=wc_order_QkkMyZ1HpfD6x', 'is_editable': False, 'needs_payment': False, 'needs_processing': True, 'date_created_gmt': '2023-03-27T17:30:57', 'date_modified_gmt': '2023-03-27T17:31:01', 'date_completed_gmt': None, 'date_paid_gmt': '2023-03-27T17:31:01', 'currency_symbol': '€', '_links': {'self': [{'href': 'https://infinity-projects.de/wp-json/wc/v3/orders/521'}], 'collection': [{'href': 'https://infinity-projects.de/wp-json/wc/v3/orders'}], 'customer': [{'href': 'https://infinity-projects.de/wp-json/wc/v3/customers/2'}]}}


if __name__ == "__main__":
    # order_id = ''.join(sys.argv[1])
    order_details = wp.get_order_id(1145)
    # # print(order_details["customer_id"])

    # #get user details from wordpress
    user_wp_details = wp.get_user_details(order_details["customer_id"])
    
    # #check if user has an account in the panel
    # #if the account isn't availabile, it'll get created
    user_panel_details = panel.check_panel_user(user_wp_details)
    
    #get every items inside the order details and handle every single one
    products = order_details['line_items']
    
    with open('./resources/website/server_templates.json', 'r') as f:
        templates = json.load(f)
        username = user_panel_details['attributes']['username']
        user_id = user_panel_details['attributes']['id']
        for i in products:
            if i['product_id'] in (a['id'] for a in templates):
                template = next((item for item in templates if item['id'] == i['product_id']),None)
                ram = template['attributes']['ram']
                disk = template['attributes']['disk']
                thread = template['attributes']['threads']
                duration = next((item for item in i['meta_data'] if item['key'] == 'Duration'),None)['value']
                
                #Create Server
                created = panel.create_new_server(username=username,user_id=user_id,ram=ram,threads=thread,disk=disk)
                print(created['attributes']['id'])
                #Process Renewal System
                processed = renewal.set_renewable(id=created['attributes']['id'], duration=duration)
                
            elif i['product_id'] == 267:
                ram = next((item for item in i['meta_data'] if item['key']=='RAM(GB)'))['value']
                thread = next((item for item in i['meta_data'] if item['key']=='Thread(s) Count'))['value']
                disk = next((item for item in i['meta_data'] if item['key']=='Storage (GB)'))['value']
                port = next((item for item in i['meta_data'] if item['key']=='Ports'))['value']
                database = next((item for item in i['meta_data'] if item['key']=='Database'))['value']
                duration = next((item for item in i['meta_data'] if item['key']=='Duration : '))['value']
                created = panel.create_new_server(username=username,user_id=user_id,ram=ram,threads=thread,disk=disk,ports=int(port),database=database)
                processed = renewal.set_renewable(id=created['attributes']['id'], duration=duration)
                
    # #Get Standalone Minecraft Details
    # order_items = next((item for item in details['line_items'] if item["product_id"] == 267), None)
    # if(order_items):
    #     panel_user_id = user_panel_details['data'][0]['attributes']['id']
    #     panel_username = user_panel_details['data'][0]['attributes']['username']
    #     ram_amount = next((item for item in order_items['meta_data'] if item['key'] == 'ram-gb'), None)['value']
    #     threads_amount = next((item for item in order_items['meta_data'] if item['key'] == 'thread-count'), None)['value']
    # print(panel.create_new_server())
    




    # Get Bungee Minecraft Details
    # print(next((item for item in details['line_items'] if item["product_id"] == 180), None))
    # if ('Minecraft' in items.values()):
    #     print("ok")
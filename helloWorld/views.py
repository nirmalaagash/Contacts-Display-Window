from django.shortcuts import render
from django.template.loader import render_to_string

from helloWorld.models import Address, Contact, Phone, Date
from django.db import connection
from collections import namedtuple
from django.http import HttpResponse

import datetime



# Create your views here.
def contactSearch(request):
    return render(request, 'contactSearch.html')


#Searches the database with the 'search' tag from the page
def contactSearchData(request):
    post = request.POST
    # print(post)
    search = post.get('Search')
    result_map = {}
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "select contact_id from contact where match(fname,mname,lname) against('" + search + "' in natural language mode);")
            contact_results = namedtuplefetchall(cursor)
            a = set()

            if len(contact_results) > 0:
                for contact in contact_results:
                    a.add(str(contact.contact_id))

            cursor.execute(
                "select contact_id from address where match(address_type,address,state,city) against('" + search + "' in natural language mode);")
            address_results = namedtuplefetchall(cursor)

            if len(address_results) > 0:
                for contact in address_results:
                    a.add(str(contact.contact_id))

            cursor.execute(
                "select contact_id from phone where match(area_code,number) against('" + search + "' in natural language mode);")
            phone_results = namedtuplefetchall(cursor)

            if len(phone_results) > 0:
                for contact in phone_results:
                    a.add(str(contact.contact_id))

            l = '(' + ', '.join(a) + ')'
            if l == '()':
                return render(request, 'contactNotFound.html', {'Result': result_map, 'search': search})
            cursor.execute("select * from contact where contact_id in " + l + ";")
            results = namedtuplefetchall(cursor)
            # print(results)
            for result in results:
                l = 1
                #   print(result)
                c_id = result.Contact_id
                result_map[c_id] = {}
                result_map[c_id]['fname'] = result.Fname
                result_map[c_id]['mname'] = result.Mname
                result_map[c_id]['lname'] = result.Lname
                cursor.execute("select * from address where contact_id = '" + str(c_id) + "';")
                address_results = namedtuplefetchall(cursor)
                if len(address_results) > l:
                    l = len(address_results)
                result_map[c_id]['addresses'] = address_results
                cursor.execute("select * from phone where contact_id = '" + str(c_id) + "';")
                phone_results = namedtuplefetchall(cursor)
                if len(phone_results) > l:
                    l = len(address_results)
                result_map[c_id]['phones'] = phone_results
                cursor.execute("select * from date where contact_id = '" + str(c_id) + "';")
                date_results = namedtuplefetchall(cursor)
                if len(address_results) > l:
                    l = len(address_results)
                result_map[c_id]['dates'] = date_results
                result_map[c_id]['l'] = l
    except:
        # print("Error")
        return render(request, 'contactNotFound.html', {'Result': result_map, 'search': search})

    return render(request, 'contactSearchData.html', {'Result': result_map, 'search': search})


#Rendering Add Contact Page
def addContact(request):
    return render(request, 'addContact.html')


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


#Index page content loading from the database
def indexNew(request):
    result_map = {}
    with connection.cursor() as cursor:

        cursor.execute(
            "select * from contact")
        results = namedtuplefetchall(cursor)
        # print(results)
        for result in results:
            l = 1
            # print(result)
            c_id = result.Contact_id
            result_map[c_id] = {}
            result_map[c_id]['fname'] = result.Fname
            result_map[c_id]['mname'] = result.Mname
            result_map[c_id]['lname'] = result.Lname
            cursor.execute("select * from address where contact_id = '" + str(c_id) + "';")
            address_results = namedtuplefetchall(cursor)
            if len(address_results) > l:
                l = len(address_results)
            result_map[c_id]['addresses'] = address_results
            cursor.execute("select * from phone where contact_id = '" + str(c_id) + "';")
            phone_results = namedtuplefetchall(cursor)
            if len(phone_results) > l:
                l = len(address_results)
            result_map[c_id]['phones'] = phone_results
            cursor.execute("select * from date where contact_id = '" + str(c_id) + "';")
            date_results = namedtuplefetchall(cursor)
            if len(address_results) > l:
                l = len(address_results)
            result_map[c_id]['dates'] = date_results
            result_map[c_id]['l'] = l
    #print(result_map)

    return render(request, 'displayDataNew.html', {'Result': result_map})


def contactAdded(request):
    # print(request.POST)
    post = request.POST
    contact = Contact(fname=post.getlist('FirstName')[0], mname=post.getlist('MiddleName')[0],
                      lname=post.getlist('LastName')[0])
    contact.save()
    c = (Contact.objects.filter(fname=post.getlist('FirstName')[0], mname=post.getlist('MiddleName')[0],
                                lname=post.getlist('LastName')[0]))[0]

    if len(post.getlist('AddressType')) > 1:
        for x in range(len(post.getlist('AddressType'))):
            address = Address(contact=c, address_type=post.getlist('AddressType')[x],
                              address=post.getlist('StreetAddress')[x],
                              state=post.getlist('City')[x], city=post.getlist('State')[x], zip=post.getlist('Zip')[x])
            address.save()
    else:
        address = Address(contact=c, address_type=post.getlist('AddressType')[0],
                          address=post.getlist('StreetAddress')[0],
                          state=post.getlist('City')[0], city=post.getlist('State')[0], zip=post.getlist('Zip')[0])
        address.save()

    if len(post.getlist('PhoneType')) > 1:
        for x in range(len(post.getlist('PhoneType'))):
            phone = Phone(contact=c, phone_type=post.getlist('PhoneType')[x],
                          area_code=post.getlist('Area')[x],
                          number=post.getlist('Number')[x])
            phone.save()
    else:
        phone = Phone(contact=c, phone_type=post.getlist('PhoneType')[0],
                      area_code=post.getlist('Area')[0],
                      number=post.getlist('Number')[0])
        phone.save()

    if len(post.getlist('DateType')) > 1:
        for x in range(len(post.getlist('DateType'))):
            d = post.getlist('selected_date')[x]
            month = d[:2]
            day = d[3:5]
            year = d[6:]
            da = year + '-' + month + '-' + day
            date = Date(contact=c, date_type=post.getlist('DateType')[x],
                        date=da)
            date.save()
    else:
        d = post.getlist('selected_date')[0]
        month = d[:2]
        day = d[3:5]
        year = d[6:]
        da = year + '-' + month + '-' + day
        date = Date(contact=c, date_type=post.getlist('DateType')[0],
                    date=da)
        date.save()
    return render(request, 'contactAdded.html')


def changeData(request):
    if request.method == 'GET':
        new_value = request.GET['newValue']
        table = request.GET['table']
        key = request.GET['key']
        field_name = request.GET['field_name']
        try:
            if new_value == 'delete':
                with connection.cursor() as cursor:
                    cursor.execute('DELETE FROM ' + table + ' WHERE ' + table + '_id = ' + str(key) + ';')
                    connection.commit()
                html = render_to_string('index.html')
                return HttpResponse(html)
        except:
            html = render_to_string('index.html')
            return HttpResponse(html)

        with connection.cursor() as cursor:
            # print('update '+table+' set '+field_name+' = "' + new_value +'" where '+table+'_id = '+ str(key)+';')
            cursor.execute(
                'update ' + table + ' set ' + field_name + ' = "' + new_value + '" where ' + table + '_id = ' + key + ';')
            connection.commit()
        html = render_to_string('index.html')
        return HttpResponse(html)


# Placeholder Values for the Modify Page
def modifyData(request):
    c_id = request.POST.getlist('contact_id')[0]
    contact = Contact.objects.filter(contact_id=c_id)
    addresses = Address.objects.filter(contact=contact[0])
    phones = Phone.objects.filter(contact=contact[0])
    dates = Date.objects.filter(contact=contact[0])

    result_map = {}
    result_map['contact_id'] = c_id
    result_map['fname'] = contact[0].fname
    result_map['mname'] = contact[0].mname
    result_map['lname'] = contact[0].lname
    result_map['address'] = []
    for address in addresses:
        temp = {}
        temp['address_id'] = address.address_id
        temp['address_type'] = address.address_type
        temp['address'] = address.address
        temp['state'] = address.state
        temp['city'] = address.city
        temp['zip'] = address.zip
        result_map['address'].append(temp)
    result_map['phone'] = []
    for phone in phones:
        temp = {}
        temp['phone_id'] = phone.phone_id
        temp['phone_type'] = phone.phone_type
        temp['area_code'] = phone.area_code
        temp['number'] = phone.number
        result_map['phone'].append(temp)
    result_map['date'] = []
    for date in dates:
        temp = {}
        temp['date_id'] = date.date_id
        temp['date_type'] = date.date_type
        temp['date'] = date.date
        result_map['date'].append(temp)
    #print(result_map)
    return render(request, 'modifyData.html', {'Result': result_map})

def modifiedData(request):
    post = request.POST
    print(post)
    with connection.cursor() as cursor:
        # print('update '+table+' set '+field_name+' = "' + new_value +'" where '+table+'_id = '+ str(key)+';')
        cursor.execute(
            "update contact set fname='"+ post.getlist('FirstName')[0] +"' , mname='"+ post.getlist('MiddleName')[0] +"' , lname='"+ post.getlist('LastName')[0] +"' where contact_id = '"+ post.getlist('contact_id')[0] +"';")

        for x in range(len(post.getlist('AddressType'))):
            cursor.execute(
                "update address set address='" + post.getlist('StreetAddress')[x] +"' , state='" +post.getlist('State')[x] +"' , city='" + post.getlist('City')[x]+"' , zip='" +post.getlist('Zip')[x] + "'where address_id='" + post.getlist('address_id')[x] +"';")

        for x in range(len(post.getlist('PhoneType'))):
            cursor.execute(
                "update phone set area_code='"+post.getlist('Area')[x] +"' , number='" +post.getlist('Number')[x] +"' where phone_id='"+ post.getlist('phone_id')[x] +"';")
        for x in range(len(post.getlist('DateType'))):
            d = post.getlist('selected_date')[0]
            month = d[:2]
            day = d[3:5]
            year = d[6:]
            da = year + '-' + month + '-' + day
            cursor.execute(
                "update date set date='"+da+"' where date_id='"+post.getlist('date_id')[x]+"';")
        connection.commit()
    return render(request, 'modifiedData.html', {})


def deleteData(request):
    c_id = request.POST.getlist('contact_id')[0]
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM contact WHERE contact_id = ' + str(c_id) + ';')
        connection.commit()
    html = render_to_string('deletedData.html')
    return HttpResponse(html)
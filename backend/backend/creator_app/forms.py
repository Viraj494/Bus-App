from django.forms import ModelForm
from .models import Passenger, Passenger_Reg, Admin_Passenger_Reg, Children_form, ChildCard_form, Adults_form, AdultsCard_form, CombinedData
from django import forms 
        

class PassengerRegForm(forms.ModelForm):
    class Meta:
        model = Passenger_Reg
        fields = ('name', 'mobile','category', 'package', 'package')
        labels ={
            'name':'Name',
            'mobile':'Mobile',
            'category':'Category',
            'package':'Package',
        }
    
    def __init__(self, *args, **kwargs):
        super(PassengerRegForm,self).__init__(*args, **kwargs)
        self.fields['mobile'].required = False        


class AdminPassengerRegForm(forms.ModelForm):
    class Meta:
        model = Admin_Passenger_Reg
        fields = ('card_id1',)  # Add a comma to make it a tuple
        labels = {
            'card_id1': 'Card ID',
        }

    def __init__(self, *args, **kwargs):
        super(AdminPassengerRegForm, self).__init__(*args, **kwargs)
        self.fields['card_id1'].required = False
        
        
LOCATIONS = [
    ('Kaduwela', 'Kaduwela'),
    ('Kothalawala', 'Kothalawala'),
    ('Malabe', 'Malabe'),
    ('Thalangama', 'Thalangama'),
    ('Koswatta', 'Koswatta'),
    ('Battaramulla', 'Battaramulla'),
    ('Welikada', 'Welikada'),
    ('Rajagiriya', 'Rajagiriya'),
    ('Ayurveda Junction', 'Ayurveda Junction'),
    ('Castle Street', 'Castle Street'),
    ('Devi Balika Junction', 'Devi Balika Junction'),
    ('Senanayake Junction (Borella)', 'Senanayake Junction (Borella)'),
    ('Horton Place', 'Horton Place'),
    ('Liberty Junction', 'Liberty Junction'),
    ('Kollupitiya (Station Road)', 'Kollupitiya (Station Road)'),
]

CAT = [
    ('Child', 'Child'),
    ('Adult', 'Adult'),
]


class PassengerForm(forms.ModelForm):
    
    p_from = forms.ChoiceField(choices=LOCATIONS, label="From")
    p_to = forms.ChoiceField(choices=LOCATIONS, label="To")
    category = forms.ChoiceField(choices=CAT, label="Passenger")
    
    class Meta:
        model = Passenger
        fields = ('name', 'category', 'card_id', 'mobile', 'email', 'address', 'p_from', 'p_to',)
        labels ={
            'name':'Name',
            'category':'Category',
            'card_id':'Card ID',
            'mobile':'Mobile',
            'email':'Email',
            'address':'Address',
            # 'p_from':'Passenger From',
            # 'p_to':'Passenger to',   
        }
    
    def __init__(self, *args, **kwargs):
        super(PassengerForm,self).__init__(*args, **kwargs)
        self.fields['card_id'].required = False
        
class CombineForm(forms.ModelForm):
    
    from_field = forms.ChoiceField(choices=LOCATIONS, label="From")
    to_field = forms.ChoiceField(choices=LOCATIONS, label="To")
    type = forms.ChoiceField(choices=CAT, label="Passenger")
    
    class Meta:
        model = Passenger
        fields = ('name', 'address', 'mobile', 'type', 'from_field',  'to_field')
        labels ={
            'name':'Name',
            'address':'Address',
            'mobile':'Mobile',
            # 'p_from':'Passenger From',
            # 'p_to':'Passenger to',   
        }
       

class ChildrenRegForm(forms.ModelForm):
    c_from = forms.ChoiceField(choices=LOCATIONS, label="From")
    c_to = forms.ChoiceField(choices=LOCATIONS, label="To")

    class Meta:
        model = Children_form
        fields = ('c_from', 'c_to')


class ChildCardForm(forms.ModelForm):
    class Meta:
        model = ChildCard_form
        fields = ('childName', 'childAddress', 'childMobile')
        labels = {
            'childName': 'Name',
            'childAddress': 'Address',
            'childMobile': 'Mobile',
        }

class AdultsRegForm(forms.ModelForm):
    a_from = forms.ChoiceField(choices=LOCATIONS, label="From")
    a_to = forms.ChoiceField(choices=LOCATIONS, label="To")

    class Meta:
        model = Adults_form
        fields = ('a_from', 'a_to')


class AdultsCardForm(forms.ModelForm):
    class Meta:
        model = AdultsCard_form
        fields = ('adultsName', 'adultsAddress', 'adultsMobile')
        labels = {
            'adultsName': 'Name',
            'adultsAddress': 'Address',
            'adultsMobile': 'Mobile',
        }      
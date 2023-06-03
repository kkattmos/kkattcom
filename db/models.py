from django.db import models
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible

# Create your models here.
class user(models.Model):
    name = models.CharField(max_length=64)
    gender = models.CharField(
        max_length=10,
        choices = [('ชาย','ชาย'),('หญิง','หญิง'),('LGBTQ+','LGBTQ+'),('ไม่ระบุ','ไม่ระบุ')],
        default = 'ไม่ระบุ'
    )
    email = models.EmailField(unique=True, blank=True)
    pwd = models.CharField(max_length=30)
    rememberme = models.BooleanField(default=False, null=True)
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
    ig = models.CharField(max_length=50, null=True, blank=True)
    igsecret = models.CharField(max_length=50,null=True)
    relation = models.CharField(max_length=20, null=True, blank=True)
    token = models.PositiveIntegerField(default=3)
    numsheetreq = models.PositiveIntegerField(default=0)
    numpresentsent = models.PositiveIntegerField(default=0)
    numsharebox = models.PositiveIntegerField(default=0)
    meetadmin = models.BooleanField(default=False)
    profilepic = models.ImageField(null=True, blank=True,upload_to='profilepic/',default='profilepic/default')

    def __str__(self):
        return f'{self.name} (ig: {self.ig})'

class errorreport(models.Model):
    user = models.CharField(max_length=65)
    code = models.CharField(max_length=2)
    page = models.CharField(max_length=2)
    error = models.CharField(max_length=100)
    details = models.CharField(max_length=500,null=True, blank=True)
    picture = models.ImageField(upload_to='errorreport/',null=True, blank=True)

    def __str__(self):
        return f'({self.code} Page {self.page}) {self.error} -> {self.details}'
class sharebox(models.Model):
    user = models.CharField(max_length=65)
    subject = models.CharField(max_length=20)
    text = models.CharField(max_length=200)
    status = models.CharField(max_length=1, default=0)

class review(models.Model):
    user = models.CharField(max_length=65)
    code = models.CharField(max_length=1)
    text = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.text}'

class kwamnaijai(models.Model):
    user = models.CharField(max_length=65)
    text = models.CharField(max_length=200)

class sheetfile(models.Model):
    code = models.CharField(max_length=1)
    order = models.CharField(max_length=1,default='0')
    theme = models.CharField(max_length=2,default='0')
    sub = models.CharField(max_length=50)
    details = models.CharField(max_length=100)
    file = models.FileField(upload_to='sheet/')

    def __str__(self):
        return f'{self.code} - {self.order} - {self.theme}'

class pack(models.Model):
    code = models.CharField(max_length=1)
    packname = models.CharField(max_length=20, default='Packname')
    grade = models.CharField(max_length=1, default='0')
    season = models.CharField(max_length=1, default='0')
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.code} ({self.count})'

class theme(models.Model):
    code = models.CharField(max_length=1, default='0')
    theme = models.CharField(max_length=30)
    preview = models.ImageField(upload_to='theme/')
    hex1 = models.CharField(max_length=7)
    hex2 = models.CharField(max_length=7)
    hex3 = models.CharField(max_length=7)
    hex4 = models.CharField(max_length=7)
    hex5 = models.CharField(max_length=7)
    hex6 = models.CharField(max_length=7)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.theme} ({self.count})'

#Problem
class giveawaycontroller(models.Model):
    active = models.BooleanField(default=False)
    warning = models.CharField(max_length=50, default=None, null=True)
    season = models.CharField(max_length=1)
    title = models.CharField(max_length=50)
    des = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.season} ({self.active})'
    
class giveawaycontroller2(models.Model):
    active = models.BooleanField(default=False)
    warning = models.CharField(max_length=50, default=None, null=True)
    season = models.CharField(max_length=1)
    title = models.CharField(max_length=50)
    des = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.season} ({self.active})'
    
class giveawayHistory(models.Model):
    userid = models.CharField(max_length=30, default='aaa')
    user = models.CharField(max_length=64 ,default='aaa')
    pack = models.CharField(max_length=1)
    theme = models.CharField(max_length=1)
    pos = models.PositiveIntegerField()
    posall = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.user} : PACK {self.pack} THEME {self.theme}'

class reviewForm(forms.Form):
    text = forms.CharField(label='มีอะไรอยากจะฝากบอกเรามั้ย?', widget=forms.Textarea(attrs={'rows':'5'}), required=True)

class sheetfileForm(forms.ModelForm):
    class Meta:
        model = sheetfile
        fields = '__all__'

class userForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ['name','gender','ig','email','pwd',]
        labels = {
            'name':'ชื่อผู้ใช้ | Username',
            'gender':'เพศ | Gender',
            'ig':'บัญชีอินสตราแกรม | IG',
            'email':'อีเมลล์ | Email',
            'pwd':'รหัสผ่าน | Password',
        }

        widgets = {
            'gender': forms.RadioSelect(),
            'email':forms.EmailInput(),
            'pwd': forms.PasswordInput(),
            'ig': forms.TextInput(attrs={'placeholder':' ไม่บังคับ'})
        }

class usereditform(forms.ModelForm):
    class Meta:
        model = user
        fields = ['name','email','ig','gender','relation']
        labels = {
            'name':'ชื่อผู้ใช้ | Username',
            'email':'อีเมลล์ | Email',
            'ig':'บัญชีอินสตราแกรม | IG',
            'gender':'เพศ | Gender',
            'relation':'ความสัมพันธ์/บทบาท | Role',
            'profilepic':'อัพโหลดรูปโปรไฟล์ | Profile Picture'
        }
        widgets = {
            'gender': forms.RadioSelect(),
            'email':forms.EmailInput(),
            'pwd': forms.PasswordInput(),
            'ig': forms.TextInput(attrs={'placeholder':' ไม่บังคับ'}),
            'profilepic': forms.ClearableFileInput(attrs={'placeholder':' ไม่บังคับ'})
        }

class changepwdForm(forms.Form):
    prepwd = forms.CharField(widget=forms.PasswordInput(),label='รหัสผ่านเดิม')
    newpwd = forms.CharField(widget=forms.PasswordInput(),label='รหัสผ่านใหม่')

class signinForm(forms.Form):
    Email = forms.EmailField()
    Password = forms.CharField(widget=forms.PasswordInput())
    # rememberme = forms.BooleanField()

class errorreportForm(forms.ModelForm):
    class Meta:
        model = errorreport
        fields = ['code','page','error','details','picture']
        labels = {
            'code':'รหัสชีทสรุปที่มีจุดผิด',
            'page':'เลขหน้าที่มีจุดผิด',
            'error':'ประโยคที่ผมเขียนผิด',
            'details':'อธิบายเพิ่มเติมถึงจุดที่พิมพ์ผิด',
            'picture':'เพิ่มภาพประกอบ (ถ้ามี)'
        }
        widgets = {
            'code':forms.TextInput(attrs={
                'placeholder':'A1'
            }),

            'page':forms.TextInput(attrs={
                'placeholder':'2'
            }),

            'error':forms.TextInput(attrs={
                'placeholder':'โพวิโดน-เบตาดีน'
            }),

            'details':forms.Textarea(attrs={
                'placeholder':'ต้องเขียนเป็น "โพวิโดน-ไอโอดีน" ซึ่งเป็นชื่อสามัญของยาตัวนี้ อย่าจำสลับกันนะ',
                'rows':'5',
                'require':'False'
            }),
        }

class shareboxForm(forms.ModelForm):
    class Meta:
        model = sharebox
        fields = ['subject','text',]
        widgets = {
            'subject':forms.TextInput(attrs={
                'placeholder':'ชื่อวิชา'
            }),

            'details':forms.Textarea(attrs={
                'placeholder':'เนื้อหาที่ต้องการเพิ่มลงชีทสรุป',
                'rows':'7',
            }),
        }

class giveawayForm(forms.Form):
    grade = forms.ChoiceField(
        label = '',
        widget = forms.Select,
        choices = [('','เลือกระดับชั้น'),('4','มัธยมศึกษาปีที่ 4'),('5','มัธยมศึกษาปีที่ 5'),('6','มัธยมศึกษาปีที่ 6'),]
        )
    theme = forms.ChoiceField(
        label = '',
        widget = forms.Select,
        choices = [
            ('','เลือกธีมสีที่ต้องการ'),
            ('0','Grayscalar'),
            ('1','Fight and Run'),
            ('2','Wild West'),
            ('3','Overcoming Danger'),
            ('4','I Am Smart'),
            ('5','Sunrise'),
            ('6','Academic'),
            ('7','Dolphins Lake'),
            ('8','Code Of Conduct'),
            ('9','Classic @studywkkattmos')]
        )
    
class giveawaycontrolForm(forms.ModelForm):
    class Meta:
        model = giveawaycontroller
        fields = '__all__'


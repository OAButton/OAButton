from django import forms


class SigninForm(forms.Form):
    PROFESSION_CHOICES = (('STUDENT', 'Student'),
                          ('DOCTOR', 'Doctor'),
                          ('PATIENT', 'Patient'),
                          ('ADVOCATE', 'Advocate'),
                          ('OTHER', 'Other'),
                          ('ACADEMIC', 'Academic'),
                          ('RESEARCHER', 'Researcher'),
                          ('BLANK', 'Prefer not to say'))

    email = forms.EmailField(required=True,
                             label='Email address',
                             widget=forms.TextInput(
                                 attrs={'placeholder': 'Email address (required)'}))
    name = forms.CharField(required=True,
                           label="Full Name",
                           widget=forms.TextInput(
                               attrs={'placeholder': 'Full Name (required)'}))

    profession = forms.ChoiceField(required=True,
                                   label="Profession",
                                   choices=PROFESSION_CHOICES)

    confirm_public = forms.BooleanField(label="I understand that information obtained by this button will be publicly accessible",
                                        required=True)

    mailinglist = forms.BooleanField(label="I would like to be added to a general OAbuton mailing list",
                                        required=False)


class Bookmarklet(forms.Form):
    user_id = forms.CharField(widget=forms.HiddenInput, required=True)

    accessed = forms.CharField( widget=forms.HiddenInput,
                               required=False)

    location = forms.CharField(required=False,
                               label="Location",
                               widget=forms.TextInput(
                                   attrs={'placeholder': "e.g. London, United Kingdom",
                                          'class': "input-block-level"}))

    coords = forms.CharField(widget=forms.HiddenInput, required=False)

    doi = forms.CharField(required=False,
                          label="DOI",
                          widget=forms.TextInput(attrs={'class': "input-block-level"}))

    url = forms.URLField(required=True,
                         label='Article URL',
                         widget=forms.HiddenInput)

    story = forms.CharField(required=False,
                            label="Why do you need access?",
                            widget=forms.Textarea(
                                attrs={'rows': "4",
                                       'placeholder': "e.g. I'm trying to save lives, dammit!",
                                       'class': "input-block-level"}))

    description = forms.CharField(required=False,
                                  label="Description",
                                  widget=forms.Textarea(
                                      attrs={'placeholder': 'Title, Authors, Journal',
                                             'data-remember': "data-remember",
                                             'rows': '4',
                                             'class': "input-block-level"}))

from django import forms


class AttachmentForm(forms.Form):
    attached_file = forms.FileField(label="File")
    title = forms.CharField(max_length=255)
    alt_text = forms.CharField(max_length=255, required=False)


class ImageAttachmentForm(forms.Form):
    attached_file = forms.ImageField(label="Image")
    title = forms.CharField(max_length=255)
    alt_text = forms.CharField(max_length=255, required=False)


class LinkAttachmentForm(forms.Form):
    url = forms.URLField()
    title = forms.CharField(max_length=255, required=False)
    text = forms.CharField(max_length=255)

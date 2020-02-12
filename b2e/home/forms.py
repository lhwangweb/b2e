from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from home.models import Urldata


class UrlForm(forms.ModelForm):
    """
    前台新增縮址表單
    """
    original_url = forms.CharField(max_length=1023)

    class Meta:
        model = Urldata
        fields = ['original_url']

    def clean_original_url(self):
        """
        URL 格式驗證
        """
        try:
            original_url = self.cleaned_data['original_url']
            u_validate = URLValidator(schemes=("http", "https"))
            u_validate(original_url)
            return original_url
        except ValidationError:
            raise forms.ValidationError("請輸入有效 URL")
            # return False
        except Exception:
            raise forms.ValidationError("URL 驗證失敗，請輸入有效 URL！")

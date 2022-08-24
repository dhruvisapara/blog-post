from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from contact.forms import ContactForm


class ContactAjax(View):
    form_class = ContactForm
    template_name = "contact.html"
    context_object_name = 'contacts'

    def get(self, *args, **kwargs):
        """This view should render template.
        """
        form = self.form_class()
        return render(self.request, self.template_name, {"contactForm": form})

    def post(self, *args, **kwargs):
        """This view should create contact model objects."""
        if self.request.method == "POST":
            form = self.form_class(self.request.POST)
            form.save()
            name1 = self.request.POST.get('name')
            email1 = self.request.POST.get('email')
            message1 = self.request.POST.get('message')
            data = {
                'name': name1,
                'email': email1,
                'message': message1,
            }
            import pdb;
            pdb.set_trace()
            return JsonResponse(
                {"success": True, "message": "Your contact details are successfully registered.", "data": data},
                status=200)
        return JsonResponse({"success": False}, status=400)

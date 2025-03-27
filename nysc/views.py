import random
import string

from django.shortcuts import render, redirect, get_object_or_404
from .models import Nysc
from .forms import NyscForm
from django.views.generic import TemplateView, DetailView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa


# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': NyscForm(request.POST)
        }
        return render(request, 'home.html', context)

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = NyscForm(request.POST)
            if form.is_valid:
                order = form.save()
                return redirect("nysc:payment", pk=order.pk)


def edit_booking(request, pk):
    product = get_object_or_404(Nysc, pk=pk)

    if request.method == 'POST':
        form = NyscForm(request.POST, instance=product)
        if form.is_valid():
            order = form.save()
            return redirect("nysc:payment", pk=order.pk)
    else:
        form = NyscForm(instance=product)

    return render(request, 'nysc/edit_booking.html', {'form': form})


class PaymentView(View):
    def get(self, request, pk, *args, **kwargs):
        order = Nysc.objects.get(pk=pk)
        context = {
            'order': order,
        }
        return render(request, 'nysc/payment.html', context)


# generate NYSC code
def code():
    order_code = ''.join(random.choices(string.digits, k=3))
    return f"N25-B1-{order_code}"


class PaymentVerifyView(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            order = Nysc.objects.get(pk=pk)
            order.payment_status = True
            order.slot = code()
            order.payment_id = request.GET.get("data")
            order.save()
            subject = "ACTIVATION CODE FOR YOUR NURU ACCOUNT"
            html_message = render_to_string('nysc/order.html', {'order': order})
            plain_message = strip_tags(html_message)
            send_mail(subject, plain_message, 'vbellotech@gmail.com', [order.email],
                      html_message=html_message)
            messages.success(self.request, "Your order was successful. We will send an email to the email address "
                                           "provided.")
            return redirect("nysc:preview", pk=order.pk)
        except ObjectDoesNotExist:
            messages.success(self.request, "Your order was not successful")
            return redirect("/")


# PREVIEW SLOT
class SlotPreviewView(View, LoginRequiredMixin):
    def get(self, request, pk, *args, **kwargs):
        order = Nysc.objects.get(pk=pk)
        context = {
            'order':order
        }
        return render(self.request, 'nysc/slot_review.html', context)


# function to convert html to pdf
def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# RENDER RESUME TO PDF
class GeneratePdf(View, LoginRequiredMixin):
    def get(self, request, pk, *args, **kwargs):
        order = Nysc.objects.get(pk=pk)
        open('templates/nysc/slotpdf.html', "w").write(render_to_string('nysc/slot_template.html',
                                                                        {
                                                                            'order': order,
                                                                        }))
        pdf = html_to_pdf('nysc/slotpdf.html')
        # return HttpResponse(pdf, content_type='application/pdf')

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "%s %s NYSC SLOT" % (order.last_name, order.first_name)
            # content = "inline; filename=%s" % (filename)
            content = "attachment; filename=%s.pdf" % (filename)
            response['Content-disposition'] = content
            return response
        return HttpResponse("Not Found")

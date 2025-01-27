from django.shortcuts import render, redirect
import paypalrestsdk
from django.conf import settings
from locations.models import SportsFieldLocation

# تكوين PayPal باستخدام التفاصيل من settings.py
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


def payment(request, field_id):
    # الحصول على بيانات الملعب باستخدام field_id
    field = SportsFieldLocation.objects.get(id=field_id)

    if request.method == 'POST':
        # إعداد الدفع عبر PayPal
        payment = paypalrestsdk.Payment({
            "intent": "sale",  # نوع الدفع (بيع)
            "payer": {
                "payment_method": "paypal"  # طريقة الدفع عبر PayPal
            },
            "transactions": [{
                "amount": {
                    "total": str(field.price_per_hour),
                    "currency": "USD"
                },
                "description": f"Payment for booking field {field.name}"
            }],
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/execute/",
                "cancel_url": "http://localhost:8000/payment/cancel/"
            }
        })

        # محاولة إنشاء عملية الدفع في PayPal
        if payment.create():
            # إذا تم إنشاء الدفع بنجاح، إعادة التوجيه إلى PayPal لإتمام الدفع
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = link.href
                    return redirect(approval_url)
        else:
            print(payment.error)  # طباعة الخطأ في حال فشل عملية الدفع

    return render(request, 'payment/payment.html', {'field': field})


def execute_payment(request):
    # الحصول على ID الدفع و PayerID من الرابط بعد العودة من PayPal
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    # العثور على عملية الدفع باستخدام paymentId
    payment = paypalrestsdk.Payment.find(payment_id)

    # محاولة تنفيذ عملية الدفع
    if payment.execute({"payer_id": payer_id}):
        # الدفع تم بنجاح
        return render(request, 'payments/payment_success.html')
    else:
        # فشل الدفع
        return render(request, 'payments/payment_failed.html')


# دالة لمعالجة الإلغاء
def payment_cancel(request):
    # عرض صفحة تُخبر المستخدم أن الدفع تم إلغاؤه
    return render(request, 'payments/payment_cancel.html')

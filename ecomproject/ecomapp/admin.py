from django.contrib import admin
from .models import *





from django.http import HttpResponse

import csv
from simple_history.admin import SimpleHistoryAdmin

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from io import BytesIO
from import_export.admin import ImportExportModelAdmin


def export_as_pdf(self, request, queryset):
    # Create a PDF file in memory
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=report.pdf'
    buffer = BytesIO()
    canvas = Canvas(buffer, pagesize=A4)

    # Draw the table data
    y = 800
    for obj in queryset:
        x = 50
        for field in field_names:
            canvas.drawString(x, y, str(getattr(obj, field)))
            x += 200
        y -= 20

    # Save the PDF to the response
    canvas.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


export_as_pdf.short_description = "Download Pdf"


def export_as_csv(self, request, queryset):
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]
    response = HttpResponse(content_type='text.csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
        meta)
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])
    return response


export_as_csv.short_description = "Download Item"


class ProductAdmin(SimpleHistoryAdmin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'quantity', 'category', 'about_to_end',
                    'jira_number','exist_in_stock', 'bar_code', 'model', 'created_at']

    actions = [export_as_csv, export_as_pdf]
    search_fields = ['name', 'quantity', 'jira_number']
    list_filter = ['created_at', 'exist_in_stock', 'category', 'about_to_end']
    list_per_page = 20
    readonly_fields = ["about_to_end"]

    prepopulated_fields = {'slug': ('name',)}
    # list_editable = ['quantity', 'exist_in_stock', 'jira_number']
    history_list_display = ['name', 'quantity',  'category', 'about_to_end',
                            'jira_number', 'bar_code', 'exist_in_stock']
                            
    def has_delete_permission(self, request, obj=None):
        return False

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'number_of_products']
    prepopulated_fields = {'slug': ('title',)}


    readonly_fields = ["number_of_products"]

    def number_of_products(self, obj):
        return obj.product_set.count()





class OrderAdmin(SimpleHistoryAdmin,admin.ModelAdmin):
    list_display = ['ordered_by', 'order_status', 'created_at',  'jira_number']
    ordering = ['-created_at']
    list_filter = ['created_at', 'order_status', 'ordered_by', "cart__cartproduct__product__category"]
    history_list_display = ['order_status']
    search_fields = ["cart__cartproduct__product__name", 'jira_number']

    list_per_page = 20

    fieldsets = (
        ('User Information', {'fields': ('username',)}),
        ('Order Status', {'fields': ('order_status',)}),
        ('Order Information', {
         'fields': ('jira_number', 'total_items', 'item_order')}),
    )

    readonly_fields = ["total_items",
                       "username", "item_order", "jira_number"]

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def username(self, obj):
        return obj.ordered_by

    def item_order(self, obj):
        all_products = obj.cart.cartproduct_set.all()
        my_str = ""
        for pro in all_products:

            my_str += f"{pro.product.name}\n\n quantity: {pro.quantity} \n"
            my_str += '...........................................\n'
        return my_str

    def total_items(self, obj):
        all_products = obj.cart.cartproduct_set.all()
        total = 0
        for single_product in all_products:
            total += single_product.quantity 
        return total




admin.site.register([Admin])

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
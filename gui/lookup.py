from ajax_select import register, LookupChannel
from gui.models import PatientProfileModel


@register('tags')
class TagsLookup(LookupChannel):

    model = PatientProfileModel

    def get_query(self, q, request):
        return self.model.objects.filter(mobile__icontains=q).order_by('mobile')[:10]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.name
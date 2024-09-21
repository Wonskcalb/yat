
from django.shortcuts import render
from django.views.generic import View

from todo.models import Item
from common.stubs import HttpResponse


def home(request):
    context = {"items": Item.objects.unchecked()}
    return render(request, "todo/index.html", context)


class ItemsListView(View):
    model = Item

    def dispatch(self, request, *args, **kwargs):
        if not request.htmx:
            return HttpResponse("")
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        match request.GET.get("state", "unchecked"):
            case "unchecked":
                items = self.model.objects.unchecked()
            case "checked":
                items = self.model.objects.checked()
            case _:
                items = self.model.objects.none()

        return render(
            request,
            template_name="todo/partial/items.html",
            context={"items": items}
        )

    def post(self, request, *args, **kwargs):
        item = self.model.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
        )
        return render(
            request,
            template_name="todo/partial/items.html",
            context={"items": [item]}
        )


class ItemDetailView(View):
    model = Item

    def dispatch(self, request, *args, **kwargs):
        if not request.htmx:
            return HttpResponse("")

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, id, *args, **kwargs):
        self.model.objects.filter(pk=id).delete()
        return HttpResponse("")

    @classmethod
    def toggle_item(cls, request, id, *args, **kwargs):
        cls.model.objects.toggle(id)
        return HttpResponse("")


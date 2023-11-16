from django.shortcuts import render
from .models import Post
from django.db.models import Q
from django.views.generic import ListView, DetailView

class PostList(ListView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_keyword = self.request.GET.get('q')
        if search_keyword:
            context['search'] = search_keyword
            context['page_url'] = f'/blog/?q={search_keyword}&page='
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_keyword = self.request.GET.get('q')
        if search_keyword:
            queryset = queryset.filter(Q(title__icontains=search_keyword) | Q(content__icontains=search_keyword)).distinct()
        return queryset
    
class PostDetail(DetailView):
    model = Post

post_list = PostList.as_view()
post_detail = PostDetail.as_view()
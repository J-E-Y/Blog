from django.shortcuts import render
from .models import Post,Category
from django.views.generic import ListView,DetailView

# Create your views here.

class PostList(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.order_by('-created')



    def get_context_data(self ,*, object_list=None, **kwargs): # 숫자 가져오는 함수 from django that it already made before

        context = super(PostList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()

        # get 하나만가져오는것
        # all 다 가져오는것
        # filter는 특정조건에 있는 것만 가져오는것

        return context

    # get 하나만가져오는것
    # all 다 가져오는것
    # filter는 특정조건에 있는 것만 가져오는것


class PostDetail(DetailView):
    model = Post



    def get_context_data(self ,*, object_list=None, **kwargs): # 숫자 가져오는 함수 from django that it already made before

        context = super(PostDetail, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()

        # get 하나만가져오는것
        # all 다 가져오는것
        # filter는 특정조건에 있는 것만 가져오는것

        return context






class PostListByCategory(ListView):

    def get_queryset(self):
        slug = self.kwargs['slug']

        if slug == '_none':
            category = None
        else:
            category = Category.objects.get(slug=slug)

        return Post.objects.filter(category=category).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['posts_without_category'] = Post.objects.filter(category=None).count()

        slug = self.kwargs['slug']

        if slug == '_none':
            context['category'] = 'unclassified'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category

        # context['title'] = 'Blog - {}'.format(category.name)
        return context









# def post_detail(request,pk):
#     blog_post =\
#         Post.objects.get(pk = pk)
#
#     return render(
# 	    request,
# 	'blog/post_detail.html',
#     {
#     'blog_post': blog_post ,
#     }
# )




# def index(request):
#     posts = Post.objects.all()
#     return render (
#
#         request,
#             'blog/index.html',
#         {
#             'posts' : posts,
#
#         }
#
#     )
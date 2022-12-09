from django.contrib.auth import get_user_model
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from blog.models import Post

user_model = get_user_model()
register = template.Library()

@register.filter#(name="author_details")
def author_details(author, current_user):
  if not isinstance(author, user_model):
      # return empty string as safe default
    return ""
  
  if current_user == author:
    return format_html("<strong>me</strong>")
  if author.first_name and author.last_name:
    name = f"{author.first_name} {author.last_name}"
  else:
    name = f"{author.username}"

  if author.email:
    prefix = format_html('<a href="mailto:{}">', author.email)
    suffix = format_html("</a>")
  else:
    prefix = ""
    suffix = ""

  return format_html('{}{}{}', prefix, name, suffix)

@register.simple_tag
def row(extra_classes=""):
    return format_html('<div class="row {}">', extra_classes)


@register.simple_tag
def endrow():
    return format_html("</div>")


@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)


@register.simple_tag
def endcol():
    return format_html("</div>")

@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
    posts = Post.objects.exclude(pk=post.pk)[:5]
    return {"title": "Recent Posts", "posts": posts}

## This contains the more complex approach for escaping and
## safe marking, instead it is recommended to use the above
## format_html function
# def author_details(post_author):
#   name = ""
#   if not isinstance(post_author, user_model):
#     return name
#   if post_author.first_name and post_author.last_name:
#     name = escape(f"{post_author.first_name} {post_author.last_name}")
#   else:
#     name = escape(f"{post_author.username}")
#   if post_author.email:
#     name = f'<a href="mailto:{escape(post_author.email)}">{name}</a>'
#   return mark_safe(name)


## This contains an alternative to implement author author_details
## filter as a template tag
# @register.simple_tag(takes_context=True)
# def author_details_tag(context):
#     request = context["request"]
#     current_user = request.user
#     post = context["post"]
#     author = post.author

#     if author == current_user:
#         return format_html("<strong>me</strong>")

#     if author.first_name and author.last_name:
#         name = f"{author.first_name} {author.last_name}"
#     else:
#         name = f"{author.username}"

#     if author.email:
#         prefix = format_html('<a href="mailto:{}">', author.email)
#         suffix = format_html("</a>")
#     else:
#         prefix = ""
#         suffix = ""

#     return format_html("{}{}{}", prefix, name, suffix)
from django.contrib.auth import get_user_model
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.html import format_html

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
# This contains the more complex approach for escaping and
# safe marking, instead it is recommended to use the above
# format_html function
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
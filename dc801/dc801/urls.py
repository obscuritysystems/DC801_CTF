from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dc801.views.home', name='home'),
    # url(r'^dc801/', include('dc801.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('ctf.urls',namespace="ctf")),
    #url(r'ctf/^', include('ctf.urls',namespace="ctf")),
    #url(r'^admin/', include(admin.site.urls)),

)

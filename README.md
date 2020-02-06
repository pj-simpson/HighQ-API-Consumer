<a href="https://highq.com/en-us/"><img src="https://1p0jkz3e2xvk1e5kpr1w6nh7-wpengine.netdna-ssl.com/wp-content/uploads/IpadPro_ProjFalcon_sm_US.png" title="HighQCollaborate"></a>


# HighQ API Consumer

This simple web app has been created by HighQ's support team, using the Django framework in order to demonstrate our RESTful API. 

Broadly speaking, HighQ Collaborate is a file-sharing, process-automation and legal service delivery platform. We provide a RESTful API to give access to most of
the system's modules and functionality. 

## Who is this for?

In support, we get a lot of queries regarding the API endpoints from people in equivalent roles to us. Whilst not nessecarily developers, per se,
there are often support, infrastructure, service desk workers, etc ,etc who have a modicum of technical curiosity and want to understand 
what is possible with the APIs we provide. 

## Imagined use case

This App is for 1st line support/ admin/ service desk employees. It is not desirable  to expose the full system admin functionality of
Collaborate to these staff, but you want them be able to carry out low-level administrative tasks like re-sending site invites, checking on the 
status and size of sites, reporting on when users were added to the system, etc, etc.

## What next?

If you are familiar with the basics of web development, you might just be curious to peek here at how we've dealt with common wed development
tasks,such as AJAX requsts to API endpoints, OAuth Token Generation and others.. 

If you are completely unfaimilar with Django and/or Python I'd reccomend working through a few of the tutorials [HERE](https://www.fullstackpython.com/django.html)
and then you can give the following a go: 

1. [Install Python 3.6](https://www.python.org/downloads/) on your local machine.
2. Clone or copy this repository. 
3. Create and activate a [virtual environment](https://docs.python-guide.org/dev/virtualenvs/) in the root folder
4. Use pip to install the [requirements.txt](http://www.learningaboutelectronics.com/Articles/How-to-create-a-requirements-txt-file-for-a-Django-project.php)
5. Add a [.env file](https://simpleisbetterthancomplex.com/2015/11/26/package-of-the-week-python-decouple.html) with the following details: 
  - HIGHQCLIENTKEY={{client_key}}
  - HIGHQCLIENTSECRET={{secret_key}}
  - HIGHQCODE={{OAuth_Code}}
  - INSTANCE={{Instance_URL}}
6. Run the application using  "python3 manage.py runserver" and visit: http://localhost:8000/

## Support 

Any questions? If you are one of our clients, please raise a ticket with support.Anything else? Contact Pete directly: 
 - support@highq.com
 - peter_joseph_simpson@hotmail.com

  

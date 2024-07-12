from django.shortcuts import render,redirect

from django.views.generic import View

from Todo.models import Todo

from django import forms

from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from django.utils import timezone

from django.utils.decorators import method_decorator

from django.contrib import messages

from django.views.decorators.cache import never_cache








def signin_required(fn):

    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:

            messages.error(request,"invalid session")

            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


decs=[signin_required,never_cache]




class TodoForm(forms.ModelForm):

    class Meta:
        model=Todo
        exclude=("created_date","user_object")
        # fields="__all__"
        # fields=["field1","field2",]
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "status":forms.Select(attrs={"class":"form-control form-select"})

        }






class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]

        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-control"}),

        }




class LoginForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))








# create your views here.
# view for listing all Todo
# url: localhost:8000/todos/all/
# method: get


@method_decorator(decs,name="dispatch")

class TodoListview(View):
    def get(self,request,*args,**kwargs):
        qs=Todo.objects.filter(user_object=request.user)

        return render(request,"todo_list.html",{"data":qs})
    




# view for creating new transaction
# url: localhost:8000/todos/add/
# method: get,post

@method_decorator(decs,name="dispatch")

class TodocreateView(View):
    def get (self,request,*args,**kwargs):
        form=TodoForm()
        return render (request,"todo_add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():

            # form.save()
            data=form.cleaned_data
            Todo.objects.create(**data,user_object=request.user)

            messages.success(request,"Todo has been added successfully")
            return redirect("todo-list")
        else:
            messages.error(request,"Failed to add todo")
            return render(request,"todo_add.html",{"form":form})





# Todo detail view
# url: localhost:8000/todos/details/
# method: get
        
@method_decorator(decs,name="dispatch")

class TodoDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todo.objects.get(id=id)
        return render (request,"todo_detail.html",{"data":qs})
    


# todo delete
# url: localhost:8000/todos/{id}}/remove/
# method get

@method_decorator(decs,name="dispatch")
   
class TodoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todo.objects.filter(id=id).delete()
        messages.success(request,"Todo has been removed")
        return redirect("todo-list")
    


# todo update
# url: localhost:8000/todos/{id}}/edit/
# method get,post
    
@method_decorator(decs,name="dispatch")

class TodoUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todo.objects.get(id=id)
        form=TodoForm(instance=todo_object)
        return render(request,"todo_edit.html",{"form":form})
    

    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_object=Todo.objects.get(id=id)

        form=TodoForm(request.POST,instance=todo_object)
        if form.is_valid():
            form.save()

            messages.success(request,"Todo has been updated successfully")          
            return redirect("todo-list")
        else:
            messages.error(request,"Failed to update todo")          
            return render(request,"todo-edit.html",{"form":form})


    

        


# signup
# url:localhost:8000/signup/
# method:get,post
        

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            # form.save()            # password encrypt
            User.objects.create_user(**form.cleaned_data)
            print("Account created")
            return redirect ("signin")
        else:
            print("failed")
            return render(request,"register.html",{"form":form})



# signin
# url:localhost:8000/signin/
# method:get,post

        
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"signin.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=u_name,password=pwd)
            if user_object:
                login(request,user_object)
                
                messages.success(request,"Signin completed successfully")               
                return redirect("todo-list")
            
        return render(request,"signin.html",{"form":form})
    



@method_decorator(decs,name="dispatch")

class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

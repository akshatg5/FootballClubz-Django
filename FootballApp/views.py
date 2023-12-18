from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import FootballClub,Player,User,Like
from .forms import PlayerForm

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user = request.user
        liked_clubs = Like.objects.filter(user=user)
        return render(request,"index.html",{"liked_clubs":liked_clubs})
    else:    
        return render(request,"index.html",{})

def clubs_list(request):
    clubs = FootballClub.objects.all().order_by('networth').reverse()
    
    #adding pagination to this web page
    paginator = Paginator(clubs,10)
    pagenum = request.GET.get('page')
    clubs_on_the_page = paginator.get_page(pagenum)
    
    return render(request,'clubs_list.html',{"clubs":clubs_on_the_page})

def club_page(request,club_id):
        club = get_object_or_404(FootballClub,pk=club_id)
        club_players = Player.objects.filter(football_club=club)
        return render(request,"club_page.html",{'club':club,'club_id':club_id,"club_players":club_players})  
     
def players(request):
    players = Player.objects.all()
    football_clubs = FootballClub.objects.all()
    return render(request,"players.html",{"players":players,"football_clubs" : football_clubs})     
    
def submit_club(request):
    if request.method == 'POST' :
        club_name = request.POST.get('clubName')
        
        if FootballClub.objects.filter(club_name=club_name).exists():
            return JsonResponse({'message': 'Club with this name already exists.'}, status=400)
        club_country = request.POST.get('clubCountry')    
        club_stadium = request.POST.get('clubStadium')
        club_logo = request.FILES.get('clubLogo')
        if FootballClub.objects.filter(club_logo=club_logo).exists():
            return JsonResponse({'message': 'Club with this logo already exists.'}, status=400)
        club_desc = request.POST.get('clubDesc')
        club_manager = request.POST.get('clubManager')
        networth = request.POST.get('networth')
        
        # make the FootballClub instance and save it
        club = FootballClub(
            club_name=club_name,
            club_country=club_country,
            club_stadium=club_stadium,
            club_logo=club_logo,
            club_desc=club_desc,
            club_manager=club_manager,
            networth=networth,
            added_by=request.user
        )
        club.save()
        
        return JsonResponse({'message':'Club Added Successfully'})
    else:
        return JsonResponse({'message':'Invalid request method. Try again!'},status=400)
    
def add_player(request):
    if request.method == "POST":
        form = PlayerForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('players')
        
    else:
        form = PlayerForm()
        
    return render(request,'players.html',{'form':form})
    
    
def like_club(request,club_id):
    user = request.user
    club = get_object_or_404(FootballClub,id=club_id)
    like, created = Like.objects.get_or_create(user=user,liked_club=club)
    
    if not created:
        like.delete()
        return JsonResponse({'liked':False})

    return JsonResponse({'liked':True}) 
    
def like_player(request):
    if request.method == 'POST':
        player_id = request.POST.get("player_id")
        user = request.user
        
        #first checking if the player exists and user is authenticated
        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return JsonResponse({"error" : "Player Not Found"})
        
        if user.is_authenticated:
            likes = Like.objects.filter(user=user,liked_player=player)
            if likes.exists():
                likes.delete()
                liked = False
            else :
                like = Like(user=user,liked_player=player)
                like.save()
                liked = True
                
            return JsonResponse({"liked":liked})
        else:
            return JsonResponse({"error":"User is not authenticated"})
    return JsonResponse({"error":"Invalid request"})

def aboutus(request):
    return render(request,"aboutus.html")

def contactus(request):
    return render(request,"contactus.html")
        
def login_view(request):
    #checking if the user made a post request
    if request.method == "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user = authenticate(request,username=username,password=password)
        
        #checking if the authentication is succesful 
        if user is not None:
            login(request,user)
            return render(request,"index.html")
        else:
            return render(request,"login.html",{"message":"Invalid username or password"})
    else:
        return render(request,"login.html")
        
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST" :
        username = request.POST["username"]
        email = request.POST["email"]
        
        #Adding the password function and checking if it verifies
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        
        if password != confirmation:
            return render(request,"register.html",{"message" :"Passwords must match!"})
        
        #Attempt to create a new user
        try:
            user = User.objects.create_user(username,email,password)
            user.save()
        except IntegrityError:
            return render(request,"register.html",{
                "message" : "Username already taken!"
            })
        login(request,user)
        return HttpResponseRedirect(reverse("index"))
    else: 
        return render(request,"register.html")
            
        

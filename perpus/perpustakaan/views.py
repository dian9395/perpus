from django.shortcuts import render, redirect, HttpResponse
from .models import Buku
from .forms import FormBuku
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from .resource import BukuResource
from django.contrib.auth.models import User

def beranda(request):
    template = 'beranda.html'
    return render(request, template)

def ekspor_xlsx(request):
    buku=BukuResource()
    dataset=buku.export()
    response=HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheet.sheet')
    response['Content-Disposition']='attachment; filename="laporan buku.xlsx"'
    return response

@login_required(login_url=settings.LOGIN_URL)
def daftar(request):
    if request.POST:
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User berhasil dibuat!")
            return redirect ('daftar')
        else:
            messages.error(request, "Terjadi kesalahan!")
            return redirect('daftar')
    else:
        form=UserCreationForm()
        konteks={
            'form':form,
        }
    return render(request,'daftar.html',konteks)

@login_required(login_url=settings.LOGIN_URL)
def pengguna(request):
    pengguna = User.objects.all()
    template = 'pengguna.html'
    context = {
        'pengguna':pengguna,
    }
    return render(request, template, context)

@login_required(login_url=settings.LOGIN_URL)
def hapus_buku(request, id_buku):
    buku=Buku.objects.filter(id=id_buku)
    buku.delete()

    return redirect('buku')

@login_required(login_url=settings.LOGIN_URL)
def ubah_buku(request, id_buku):
    buku=Buku.objects.get(id=id_buku)
    template='ubah-buku.html'
    if request.POST:
        form=FormBuku(request.POST, request.FILES, instance=buku)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Berhasil diperbarui")
            return redirect('ubah_buku', id_buku=id_buku)
    else:
        form=FormBuku(instance=buku)
        konteks={
            'form':form,
            'buku':buku,
        }
    return render(request,template,konteks)

@login_required(login_url=settings.LOGIN_URL)
def buku (request):

    # judul=["Belajar Django","Belajar Python","Belajar Bootstrap"]
    # penulis="Dian Arianto"

    # select*from Buku where jumlah=90
    # inner join kelompok.id=buku.kelompok_id where kelompok.nama='Produktif'
    # limit 3
    books = Buku.objects.all()

    konteks = {
        'books': books,
    }
    return render(request, 'buku.html', konteks) 

def penerbit (request):

    return render(request, 'penerbit.html')


def penulis (request):
    return HttpResponse('Halaman Penulis')

@login_required(login_url=settings.LOGIN_URL)
def tambah_buku(request):
    if request.POST:
        form = FormBuku(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form=FormBuku()
            pesan="Data berhasil disimpan"

            konteks={
                'form': form,
                'pesan': pesan,
            }
            return render(request, 'tambah-buku.html', konteks)


    else:
        form=FormBuku()
        konteks={
            'form': form,
        }
    return render(request, 'tambah-buku.html', konteks)
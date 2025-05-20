from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import uuid
from django.utils.text import slugify
import random, string



ROLE_CHOICES = [
    ('super_admin', 'Super Admin'),
    ('admin_prov', 'Admin Kabupaten'),
    ('admin_kab', 'Admin Kecamatan')
]

class Master_UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, phone, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        if not phone:
            raise ValueError('The Phone field must be set')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_verified', False)
        return self._create_user(email, username, phone, password, **extra_fields)

    def create_superuser(self, email, username, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_verified') is not True:
            raise ValueError('Superuser must have is_verified=True.')

        return self._create_user(email, username, phone, password, **extra_fields)

class CreateUpdateTime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    archive_at = models.DateTimeField(default=None, null=True)
    deleted_at = models.DateTimeField(default=None, null=True)

    class Meta:
        abstract = True

class Tahun(models.Model):
    tahun = models.IntegerField(default=2024)

    class Meta:
        abstract = True

class Master_User(AbstractBaseUser, CreateUpdateTime):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=50)
    alamat = models.TextField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, upload_to='images/avatar/', default='images/avatar/avatar-default.svg')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user')
    email_verification_token = models.CharField(max_length=100, default='')

    objects = Master_UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone', 'role', 'is_superuser']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True




def rand_slug():
	rand = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
	return rand.lower()

class Wisata(CreateUpdateTime):
    KATEGORI_CHOICES = [
        ('bahari', 'Bahari'),
        ('sejarah', 'Sejarah'),
        ('kuliner', 'Kuliner'),
    ]

    wisata_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    nama_wisata = models.CharField(max_length=255)
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES)
    deskripsi = models.TextField()
    fasilitas = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    alamat = models.TextField()
    maps = models.URLField()
    harga = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    embed_maps = models.TextField(blank=True, null=True)
    jam_operasional = models.CharField(max_length=100, blank=True, null=True)


    def _str_(self):
        return self.nama_wisata

    def _init_(self, *args, **kwargs):
        super(Wisata, self)._init_(*args, **kwargs)
        self.old_nama_wisata = self.nama_wisata

    def save(self, *args, **kwargs):
        # Cek apakah slug masih kosong
            if not self.slug:
                base_slug = slugify(self.nama_wisata)
                slug = base_slug
                while Wisata.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    slug = f"{base_slug}-{rand_slug()}"
                self.slug = slug
                print("Generated slug:", self.slug)  # debug
            
            else:
                old_obj = Wisata.objects.filter(pk=self.pk).first()
                if old_obj and old_obj.nama_wisata != self.nama_wisata:
                    # Nama berubah, regenerasi slug
                    base_slug = slugify(self.nama_wisata)
                    slug = base_slug
                    while Wisata.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                        slug = f"{base_slug}-{rand_slug()}"
                    self.slug = slug

            super(Wisata, self).save(*args, **kwargs)

class WisataImage(models.Model):
    wisata = models.ForeignKey(Wisata, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True,upload_to='wisata/images')



class Penginapan(CreateUpdateTime):
    penginapan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    nama_penginapan = models.CharField(max_length=255)
    deskripsi = models.TextField()
    fasilitas = models.TextField()
    alamat = models.TextField()
    maps = models.URLField()
    harga = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    slug = models.SlugField(unique=True, blank=True)
    embed_maps = models.TextField(blank=True, null=True)
    no_telepon = models.TextField(blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nama_penginapan)
            slug = base_slug
            while Penginapan.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{rand_slug()}"
            self.slug = slug
        else:
            old_obj = Penginapan.objects.filter(pk=self.pk).first()
            if old_obj and old_obj.nama_penginapan != self.nama_penginapan:
                base_slug = slugify(self.nama_penginapan)
                slug = base_slug
                while Penginapan.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    slug = f"{base_slug}-{rand_slug()}"
                self.slug = slug

        super(Penginapan, self).save(*args, **kwargs)

    def __str__(self):
        return self.nama_penginapan



class PenginapanImage(models.Model):
    penginapan = models.ForeignKey(Penginapan, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True,upload_to='penginapan/images')

class Faq(CreateUpdateTime):
    pertanyaan = models.TextField()
    jawaban = models.TextField()

class Kritiksaran(CreateUpdateTime):
    pengguna = models.ForeignKey(Master_User, on_delete=models.CASCADE,  null=True, blank=True)
    kritik = models.TextField()


class Kontak(CreateUpdateTime):
    alamat = models.TextField()  # Menyimpan alamat
    email = models.EmailField(unique=True)  # Menyimpan email dengan validasi unik
    phone = models.CharField(max_length=15)  # Menyimpan nomor telepon
    instagram = models.URLField()  # Menyimpan URL Instagram
    youtube = models.URLField()  # Menyimpan URL Youtube
    jam_operasional = models.CharField(max_length=100, null=True, blank=True)
    link_maps = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Kontak: {self.phone} - {self.email}"



class Berita(models.Model):
    KATEGORI_CHOICES = [
        ('berita', 'Berita'),
        ('event', 'Event'),
    ]

    berita_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='berita/thumbnails/')
    konten = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    tags = models.CharField(max_length=255, help_text="Pisahkan dengan koma (,) jika lebih dari satu tag")
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES)
    created_by = models.CharField(max_length=100)
    last_updated_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            while Berita.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{rand_slug()}"
            self.slug = slug
        else:
            old_obj = Berita.objects.filter(pk=self.pk).first()
            if old_obj and old_obj.title != self.title:
                base_slug = slugify(self.title)
                slug = base_slug
                while Berita.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    slug = f"{base_slug}-{rand_slug()}"
                self.slug = slug
        super(Berita, self).save(*args, **kwargs)

class Infografis(models.Model):
    infografis_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    gambar = models.ImageField(upload_to='infografis/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Infografis'
        verbose_name_plural = 'Infografis'
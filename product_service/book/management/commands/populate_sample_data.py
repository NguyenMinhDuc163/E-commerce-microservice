from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
import os
from datetime import date, datetime
from book.models import Book, Author, Publisher, Category
from mobile.models import Mobile, Producer
from clothes.models import Clothes, Brand


class Command(BaseCommand):
    help = 'Populate database with sample data for all product types'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate sample data...'))
        
        # Create sample data for Books
        self.create_books()
        
        # Create sample data for Mobiles
        self.create_mobiles()
        
        # Create sample data for Clothes
        self.create_clothes()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated sample data!'))

    def create_books(self):
        self.stdout.write('Creating sample books...')
        
        # Sample Authors
        authors_data = [
            {'name': 'Nguyễn Nhật Ánh', 'birth_date': date(1955, 5, 7)},
            {'name': 'Tô Hoài', 'birth_date': date(1920, 9, 27)},
            {'name': 'Nam Cao', 'birth_date': date(1915, 10, 29)},
            {'name': 'Xuân Quỳnh', 'birth_date': date(1942, 10, 8)},
        ]
        
        for author_data in authors_data:
            Author.objects.get_or_create(**author_data)
        
        # Sample Publishers
        publishers_data = [
            {'name': 'NXB Trẻ', 'phone_number': '0283932344', 'address': '161B Lý Chính Thắng, Quận 3, TP.HCM'},
            {'name': 'NXB Kim Đồng', 'phone_number': '0246256347', 'address': '55 Quang Trung, Hai Bà Trưng, Hà Nội'},
            {'name': 'NXB Văn học', 'phone_number': '0248225340', 'address': '18 Nguyễn Trường Tộ, Ba Đình, Hà Nội'},
        ]
        
        for pub_data in publishers_data:
            Publisher.objects.get_or_create(**pub_data)
        
        # Sample Categories
        categories_data = [
            {'name': 'Văn học'},
            {'name': 'Thiếu nhi'},
            {'name': 'Giáo dục'},
            {'name': 'Kỹ năng sống'},
        ]
        
        for cat_data in categories_data:
            Category.objects.get_or_create(**cat_data)
        
        # Sample Books
        books_data = [
            {
                'title': 'Dế Mèn Phiêu Lưu Ký',
                'description': 'Câu chuyện về chú dế mèn dũng cảm và những cuộc phiêu lưu thú vị.',
                'published_date': date(2010, 5, 15),
                'quantity': 100,
                'price': 50000,
                'author': 'Tô Hoài',
                'publisher': 'NXB Kim Đồng',
                'categories': 'Thiếu nhi',
                'type': 'book'
            },
            {
                'title': 'Tôi Thấy Hoa Vàng Trên Cỏ Xanh',
                'description': 'Tác phẩm kinh điển của Nguyễn Nhật Ánh về tuổi thơ miền quê.',
                'published_date': date(2015, 8, 20),
                'quantity': 150,
                'price': 75000,
                'author': 'Nguyễn Nhật Ánh',
                'publisher': 'NXB Trẻ',
                'categories': 'Văn học',
                'type': 'book'
            },
            {
                'title': 'Chí Phèo',
                'description': 'Tác phẩm nổi tiếng của Nam Cao về số phận con người.',
                'published_date': date(2020, 3, 10),
                'quantity': 80,
                'price': 45000,
                'author': 'Nam Cao',
                'publisher': 'NXB Văn học',
                'categories': 'Văn học',
                'type': 'book'
            },
            {
                'title': 'Sóng',
                'description': 'Tập thơ nổi tiếng của Xuân Quỳnh.',
                'published_date': date(2018, 12, 5),
                'quantity': 60,
                'price': 35000,
                'author': 'Xuân Quỳnh',
                'publisher': 'NXB Văn học',
                'categories': 'Văn học',
                'type': 'book'
            },
            {
                'title': 'Cô Gái Đến Từ Hôm Qua',
                'description': 'Tiểu thuyết lãng mạn của Nguyễn Nhật Ánh.',
                'published_date': date(2016, 6, 18),
                'quantity': 120,
                'price': 65000,
                'author': 'Nguyễn Nhật Ánh',
                'publisher': 'NXB Trẻ',
                'categories': 'Văn học',
                'type': 'book'
            }
        ]
        
        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
            if created:
                self.stdout.write(f'  Created book: {book.title}')

    def create_mobiles(self):
        self.stdout.write('Creating sample mobiles...')
        
        # Sample Producers
        producers_data = [
            {
                'name': 'Apple',
                'description': 'Công ty công nghệ hàng đầu thế giới',
                'address': 'Cupertino, California, USA',
                'phone_number': '+1-800-275-2273',
                'email': 'info@apple.com',
                'website': 'https://www.apple.com'
            },
            {
                'name': 'Samsung',
                'description': 'Tập đoàn điện tử đa quốc gia Hàn Quốc',
                'address': 'Seoul, South Korea',
                'phone_number': '+82-2-2255-0114',
                'email': 'info@samsung.com',
                'website': 'https://www.samsung.com'
            },
            {
                'name': 'Xiaomi',
                'description': 'Công ty công nghệ Trung Quốc',
                'address': 'Beijing, China',
                'phone_number': '+86-400-100-5678',
                'email': 'info@xiaomi.com',
                'website': 'https://www.xiaomi.com'
            }
        ]
        
        for producer_data in producers_data:
            Producer.objects.get_or_create(
                name=producer_data['name'],
                defaults=producer_data
            )
        
        # Sample Mobiles
        mobiles_data = [
            {
                'name': 'iPhone 15 Pro Max',
                'description': 'Điện thoại cao cấp nhất của Apple với chip A17 Pro',
                'price': 32000000,
                'sale': 30000000,
                'color': 'Titan Tự Nhiên',
                'quantity': 50,
                'producer': 'Apple',
                'type': 'mobile'
            },
            {
                'name': 'iPhone 15',
                'description': 'iPhone thế hệ mới với nhiều cải tiến',
                'price': 25000000,
                'sale': 24000000,
                'color': 'Xanh',
                'quantity': 75,
                'producer': 'Apple',
                'type': 'mobile'
            },
            {
                'name': 'Samsung Galaxy S24 Ultra',
                'description': 'Flagship Android cao cấp với S Pen',
                'price': 31000000,
                'sale': 29000000,
                'color': 'Đen Titan',
                'quantity': 60,
                'producer': 'Samsung',
                'type': 'mobile'
            },
            {
                'name': 'Samsung Galaxy S24',
                'description': 'Smartphone Android mạnh mẽ',
                'price': 22000000,
                'sale': 21000000,
                'color': 'Tím',
                'quantity': 80,
                'producer': 'Samsung',
                'type': 'mobile'
            },
            {
                'name': 'Xiaomi 14 Ultra',
                'description': 'Camera chuyên nghiệp với Leica',
                'price': 28000000,
                'sale': 26000000,
                'color': 'Trắng',
                'quantity': 40,
                'producer': 'Xiaomi',
                'type': 'mobile'
            },
            {
                'name': 'Xiaomi Redmi Note 13',
                'description': 'Smartphone tầm trung giá tốt',
                'price': 6000000,
                'sale': 5500000,
                'color': 'Xanh Dương',
                'quantity': 100,
                'producer': 'Xiaomi',
                'type': 'mobile'
            }
        ]
        
        for mobile_data in mobiles_data:
            mobile, created = Mobile.objects.get_or_create(
                name=mobile_data['name'],
                defaults=mobile_data
            )
            if created:
                self.stdout.write(f'  Created mobile: {mobile.name}')

    def create_clothes(self):
        self.stdout.write('Creating sample clothes...')
        
        # Sample Brands
        brands_data = [
            {
                'name': 'Nike',
                'description': 'Thương hiệu thể thao hàng đầu thế giới'
            },
            {
                'name': 'Adidas',
                'description': 'Thương hiệu thể thao nổi tiếng từ Đức'
            },
            {
                'name': 'Uniqlo',
                'description': 'Thương hiệu thời trang bình dân từ Nhật Bản'
            },
            {
                'name': 'Zara',
                'description': 'Thương hiệu thời trang nhanh từ Tây Ban Nha'
            }
        ]
        
        for brand_data in brands_data:
            Brand.objects.get_or_create(
                name=brand_data['name'],
                defaults=brand_data
            )
        
        # Sample Clothes
        clothes_data = [
            {
                'name': 'Nike Air Force 1',
                'size': '42',
                'description': 'Giày thể thao kinh điển của Nike',
                'price': 2500000,
                'sale': 2200000,
                'color': 'Trắng',
                'quantity': 30,
                'brand': 'Nike',
                'type': 'clothes'
            },
            {
                'name': 'Nike Dri-FIT T-Shirt',
                'size': 'L',
                'description': 'Áo thun thể thao với công nghệ Dri-FIT',
                'price': 800000,
                'sale': 720000,
                'color': 'Đen',
                'quantity': 50,
                'brand': 'Nike',
                'type': 'clothes'
            },
            {
                'name': 'Adidas Ultraboost 22',
                'size': '41',
                'description': 'Giày chạy bộ cao cấp',
                'price': 4500000,
                'sale': 4000000,
                'color': 'Xám',
                'quantity': 25,
                'brand': 'Adidas',
                'type': 'clothes'
            },
            {
                'name': 'Adidas 3-Stripes Track Jacket',
                'size': 'M',
                'description': 'Áo khoác thể thao cổ điển',
                'price': 1800000,
                'sale': 1600000,
                'color': 'Xanh Navy',
                'quantity': 40,
                'brand': 'Adidas',
                'type': 'clothes'
            },
            {
                'name': 'Uniqlo Heattech Ultra Warm Crew Neck T-Shirt',
                'size': 'XL',
                'description': 'Áo giữ nhiệt cao cấp',
                'price': 590000,
                'sale': 490000,
                'color': 'Đen',
                'quantity': 60,
                'brand': 'Uniqlo',
                'type': 'clothes'
            },
            {
                'name': 'Uniqlo Slim Fit Jeans',
                'size': '32',
                'description': 'Quần jeans ôm vừa phải',
                'price': 1200000,
                'sale': 990000,
                'color': 'Xanh Đậm',
                'quantity': 45,
                'brand': 'Uniqlo',
                'type': 'clothes'
            },
            {
                'name': 'Zara Basic T-Shirt',
                'size': 'S',
                'description': 'Áo thun basic đa năng',
                'price': 400000,
                'sale': 320000,
                'color': 'Trắng',
                'quantity': 70,
                'brand': 'Zara',
                'type': 'clothes'
            },
            {
                'name': 'Zara Skinny Jeans',
                'size': '30',
                'description': 'Quần jeans skinny thời trang',
                'price': 1100000,
                'sale': 880000,
                'color': 'Đen',
                'quantity': 35,
                'brand': 'Zara',
                'type': 'clothes'
            }
        ]
        
        for clothes_data in clothes_data:
            clothes, created = Clothes.objects.get_or_create(
                name=clothes_data['name'],
                defaults=clothes_data
            )
            if created:
                self.stdout.write(f'  Created clothes: {clothes.name}') 
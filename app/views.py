from django.shortcuts import render, redirect
from app.forms import DataForm
from app.models import Data
import csv
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import requests
from django.core.files.storage import FileSystemStorage
from sklearn.preprocessing import LabelEncoder
from django.core.paginator import Paginator
from django.shortcuts import render
from sklearn.metrics import accuracy_score

# Create your views here.

def index(request):
    datas = Data.objects.all()
    return render(request, "app/index.html", {"datas": datas})

def data(request):
    data_list = Data.objects.all()
    paginator = Paginator(data_list, 50) 
    page = request.GET.get('page')
    datas = paginator.get_page(page)
    return render(request, "app/data.html", {"datas": datas})

def addnew(request):
    if request.method == "POST":
        form = DataForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('data')
            except:
                pass
    else:
        form = DataForm()
    return render(request, "app/tambahdata.html", {"form":form})

def edit(request, id):
    data = Data.objects.get(id=id)
    return render(request, "app/edit.html", {"data":data})

def update(request, id):
    data = Data.objects.get(id=id)
    form = DataForm(request.POST, instance = data)
    if form.is_valid():
        form.save()
        return redirect("data")
    return render(request, "app/edit.html", {"data":data})

def destroy(request, id):
    data = Data.objects.get(id=id)
    data.delete()
    return redirect("data")

def process_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]
        csv_data = csv.reader(csv_file.read().decode("utf-8").splitlines())
        header = next(csv_data)

        for row in csv_data:
            Data.objects.create(
                dur=row[0],
                proto=row[1],
                service=row[2],
                state=row[3],
                spkts=row[4],
                dpkts=row[5],
                sbytes=row[6],
                dbytes=row[7],
                rate=row[8],
                sttl=row[9],
                dttl=row[10],
                sload=row[11],
                dload=row[12],
                sloss=row[13],
                dloss=row[14],
                sinpkt=row[15],
                dinpkt=row[16],
                sjit=row[17],
                djit=row[18],
                swin=row[19],
                stcpb=row[20],
                dtcpb=row[21],
                dwin=row[22],
                tcprtt=row[23],
                synack=row[24],
                ackdat=row[25],
                smean=row[26],
                dmean=row[27],
                trans_depth=row[28],
                response_body_len=row[29],
                ct_srv_src=row[30],
                ct_state_ttl=row[31],
                ct_dst_ltm=row[32],
                ct_src_dport_ltm=row[33],
                ct_dst_sport_ltm=row[34],
                ct_dst_src_ltm=row[35],
                is_ftp_login=row[36],
                ct_ftp_cmd=row[37],
                ct_flw_http_mthd=row[38],
                ct_src_ltm=row[39],
                ct_srv_dst=row[40],
                is_sm_ips_ports=row[41],
                attack_cat=row[42],
                label=row[43],
            )

        return redirect("data")

    return redirect("upload_csv")


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")  # Redirect to desired page after successful login
    else:
        form = AuthenticationForm()
    return render(request, "app/signin.html", {"form": form})
    
def signup(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/")
        else:
            return render(request, 'app/signup.html', {"form":form})
    else:
        form = UserCreationForm()
        return render(request, 'app/signup.html', {'form':form})
    
def signout(request):
    logout(request)
    return redirect("signin")

def prepare_data(data):
    # Pilih fitur-fitur yang akan digunakan sebagai input model
    features = data[[
        "dur", "spkts", "dpkts", "sbytes", "dbytes", "rate", "sttl",
        "dttl", "sload", "dload", "sloss", "dloss", "sinpkt", "dinpkt", "sjit", "djit", "swin",
        "stcpb", "dtcpb", "dwin", "tcprtt", "synack", "ackdat", "smean", "dmean", "trans_depth",
        "response_body_len", "ct_srv_src", "ct_state_ttl", "ct_dst_ltm", "ct_src_dport_ltm",
        "ct_dst_sport_ltm", "ct_dst_src_ltm", "is_ftp_login", "ct_ftp_cmd", "ct_flw_http_mthd",
        "ct_src_ltm", "ct_srv_dst", "is_sm_ips_ports"
    ]].values

    # Pilih kolom "attack_cat" atau "label" sebagai label (tergantung pada kebutuhan)
    labels = data["label"]  # Ubah menjadi "label" jika ingin menggunakan kolom label

    # Kodekan label menjadi nilai numerik menggunakan LabelEncoder
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)

    # Lakukan label encoding pada atribut yang memerlukan
    #proto_encoder = LabelEncoder()
    #service_encoder = LabelEncoder()
    #state_encoder = LabelEncoder()
    # attack_cat_encoder =  LabelEncoder()

    #features[:, 0] = proto_encoder.fit_transform(features[:, 0])  # source_ip
    #features[:, 1] = service_encoder.fit_transform(features[:, 1])  # destination_ip
    #features[:, 2] = state_encoder.fit_transform(features[:, 2])  # protocol
    # features[:, 3] = attack_cat_encoder.fit_transform(features[:, 3])  # flag_packet

    return features, labels_encoded

def save_results(predictions):
    # Simpan hasil prediksi ke dalam database
    pass

def ip_to_float(ip):
    # Lakukan operasi yang sesuai untuk string IP di sini
    # Misalnya, Anda dapat membagi IP menjadi bagian-bagian dan melakukan operasi numerik pada setiap bagian.
    ip_parts = ip.split('.')
    # Contoh: Mengambil jumlah dari bagian-bagian IP
    ip_sum = sum(int(part) for part in ip_parts)
    return ip_sum

def perform_detection(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        csv_file = request.FILES["csv_file"]
        csv_data = csv.reader(csv_file.read().decode("utf-8").splitlines())
        header = next(csv_data)

        # Ambil data dari tabel data di database
        data_objects = Data.objects.all()

        # Konversi data dari model menjadi DataFrame Pandas
        data_df = pd.DataFrame(list(data_objects.values()))

        # Persiapkan data dan label untuk training
        X_train, y_train = prepare_data(data_df)

        # Buat dan latih model Random Forest
        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        # Proses data uji dari file CSV menjadi fitur numerik
        test_data = []
        for row in csv_data:
            dur = float(row[0])
            spkts = int(row[1])
            dpkts = int(row[2])
            sbytes = int(row[3])
            dbytes = int(row[4])
            rate = float(row[5])
            sttl = int(row[6])
            dttl = int(row[7])
            sload = float(row[8])
            dload = float(row[9])
            sloss = int(row[10])
            dloss = int(row[11])
            sinpkt = float(row[12])
            dinpkt = float(row[13])
            sjit = float(row[14])
            djit = float(row[15])
            swin = int(row[16])
            stcpb = int(row[17])
            dtcpb = int(row[18])
            dwin = int(row[19])
            tcprtt = float(row[20])
            synack = float(row[21])
            ackdat = float(row[22])
            smean = float(row[23])
            dmean = float(row[24])
            trans_depth = int(row[25])
            response_body_len = int(row[26])
            ct_srv_src = int(row[27])
            ct_state_ttl = int(row[28])
            ct_dst_ltm = int(row[29])
            ct_src_dport_ltm = int(row[30])
            ct_dst_sport_ltm = int(row[31])
            ct_dst_src_ltm = int(row[32])
            is_ftp_login = int(row[33])
            ct_ftp_cmd = int(row[34])
            ct_flw_http_mthd = int(row[35])
            ct_src_ltm = int(row[36])
            ct_srv_dst = int(row[37])
            is_sm_ips_ports = int(row[38])
            source_ip = row[39]  # Ganti indeks dengan indeks kolom yang sesuai
            destination_ip = ip_to_float(row[40])

            # Gabungkan atribut yang telah di-encode dengan atribut numerik lainnya
            test_data_encoded = np.column_stack((dur, spkts, dpkts, sbytes, dbytes, rate, sttl, dttl,
                                                sload, dload, sloss, dloss, sinpkt, dinpkt, sjit, djit,
                                                swin, stcpb, dtcpb, dwin, tcprtt, synack, ackdat, smean,
                                                dmean, trans_depth, response_body_len, ct_srv_src,
                                                ct_state_ttl, ct_dst_ltm, ct_src_dport_ltm, ct_dst_sport_ltm,
                                                ct_dst_src_ltm, is_ftp_login, ct_ftp_cmd, ct_flw_http_mthd,
                                                ct_src_ltm, ct_srv_dst, is_sm_ips_ports))

            # Pastikan data uji memiliki bentuk 2D yang sesuai dengan data latih
            test_data_encoded = test_data_encoded.reshape(1, -1)
            print(data_df.head())

            # Inisialisasi objek LabelEncoder
            label_encoder = LabelEncoder()
            source_ip_encoder = label_encoder.fit_transform(data_df["source_ip"])

            # Transformasi label kelas menjadi angka
            labels_encoded = label_encoder.fit_transform(data_df["attack_cat"])
            
            # Lakukan prediksi pada data uji
            predictions = model.predict(test_data_encoded)

            # Tambahkan kode untuk mengonversi prediksi kembali ke label asli
            predicted_labels = label_encoder.inverse_transform(predictions).tolist()

            # Simpan hasil prediksi ke dalam database atau tampilkan pada halaman index.html
            save_results(predicted_labels)

            # Tambahkan kode untuk melihat jumlah elemen dalam predictions
            num_predictions = len(predictions)
            print(f"Jumlah elemen dalam predictions: {num_predictions}")
            print(f"Source IP: {source_ip_encoder}")
            print(f"Destination IP: {destination_ip}")

            # Ganti dengan label sebenarnya jika tersedia
            #true_labels = ["Normal"]

            # Simpan hasil prediksi ke dalam database atau tampilkan pada halaman index.html
            #save_results(predictions)

            # Hitung akurasi jika Anda memiliki label sebenarnya
            #accuracy = accuracy_score(true_labels, predictions)

            # Hitung akurasi deteksi
            # y_true = [label_encoder.transform(data_df["label"])]  # Label sebenarnya dari data latih
            # accuracy = accuracy_score(y_train, predictions)
            #true_labels = data_df["label"].tolist()
            #accuracy = accuracy_score(true_labels, predicted_labels)

            # Hitung akurasi deteksi
            # accuracy = calculate_detection_accuracy(predictions)

            result = {
                "message": "Deteksi selesai",
                "predictions": predicted_labels,
                #"accuracy": accuracy,
                "destination_ip": destination_ip,
                "source_ip": source_ip,
            }
            return JsonResponse(result)
    else:
        datas = Data.objects.all()
        return render(request, "app/index.html", {"datas": datas})
    
def calculate_detection_accuracy(predictions):
    # Anda perlu memiliki label yang benar atau data sebenarnya untuk menghitung akurasi
    # Di sini, kita asumsikan label yang benar adalah "Normal" untuk semua data uji
    true_labels = ["Normal"] * len(predictions)

    # Hitung akurasi dengan membandingkan prediksi dengan label sebenarnya
    accuracy = accuracy_score(true_labels, predictions)

    # Konversi hasil akurasi menjadi persentase
    accuracy_percentage = accuracy * 100

    return accuracy_percentage
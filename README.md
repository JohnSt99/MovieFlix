# MovieFlix2020_E17144_Stylianou_Ioannis
Απαλλακτική εργασία πληροφοριακών συστημάτων
Python
-
#### Requirements
- click==7.1.2
- Flask==1.1.2
- itsdangerous==1.1.0
- Jinja2==2.11.2
- MarkupSafe==1.1.1
- pymongo==3.10.1
- Werkzeug==1.0.1

Docker
-
Εγκατάσταση Docker / Docker Toolbox
#### Απαιτήσεις συστήματος:

- 64-bit processor με Second Level Address Translation (SLAT)
- 4GB system RAM
- BIOS-level hardware virtualization support πρέπει να είναι ενεργοποιημένο στις ρυθμίσεις του BIOS (συνήθως είναι ήδη activated)

#### Εγκατάσταση στα Windows:

Πρέπει να έχετε Windows 10 Pro, Windows 10 Student edition - Σε Windows Home δεν θα μπορέσει να γίνει εγκατάσταση σωστά
Πρέπει επίσης να είναι ενεργοποιημένα τα:

- Hyper-V
- Containers Windows Features

Κατεβάζετε το εκτελέσιμο αρχείο από εδώ: https://hub.docker.com/editions/community/docker-ce-desktop-wind 

#### Εγκατάσταση στα Linux (Ubuntu):

Αρκεί να εκτελέσετε τις παρακάτω εντολές στο terminal:
```
sudo apt-get update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository -y "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt install docker-ce
```

#### Βασικές εντολές Docker
- Προβολή λίστας με όλα τα images που έχουμε τοπικά στον υπολογιστή μας: `docker images`
- Εμφάνιση λίστας με όλα τα container που έχουμε στον υπολογιστή μας: `docker ps -a`
- Δημιουργία και εκτέλεση container (Αν δεν υπάρχει ήδη τοπικά στον υπολογιστή, θα γίνει και κατέβασμα): `docker run image_name --name friendly_name -p HOST_PORT:DOCKER_PORT`
- Εκτέλεση εντολών μέσα σε ένα container: `docker exec friendly_name`
- Παύση ενός container: `docker stop friendly_name`
- Αφαίρεση ενός σταματημένου container: `docker rm friendly_name`
- Διαγραφή ενός image από τον υπολογιστή (αφού πρώτα έχει διαγραφεί το container που το χρησιμοποιεί): `docker rmi image_name`
- Εμφάνιση low-level πληροφοριών για ένα container: `docker inspect friendly_name`
- Εμφάνιση log για ένα container: `docker log friendly_name`
- Build από Dockerfile: `docker build -t image_name .`
- . στο τέλος βάζουμε αν το Dockerfile είναι στο ίδιο μέρος με το path που έχουμε στο terminal.
- Ενναλακτικά, αντικαθιστούμε το . με το path για το Dockerfile

#### Δημιουργία Dockerfile
Προσοχή: Το Dockerfile δεν έχει κάποιο extension!

#### Linux:

Για να το δημιουργήσουμε πρέπει να εκτελέσουμε τη παρακάτω εντολή στο terminal: touch Dockerfile

#### Windows:

- Δημιουργούμε ένα κενό txt αρχείο (πχ στο Notepad) και το αποθηκεύουμε χωρίς extension:
- File / Save as / File name: Dockerfile
- Και επιλέγουμε Save as type: All Files (*.*)

#### Βασικές εντολές που θα χρησιμοποιήσουμε σε ένα Dockerfile:

- Ποια είναι η base image που χρησιμοποιείται (πρέπει πάντα να υπάρχει σε ένα Dockerfile και το βάζουμε στη πρώτη γραμμή): `FROM ubuntu:16.04`
- Όνομα και email του maintainer του image: `MAINTAINER name <email@address.domain>`
- Αντιγραφή αρχείων από τον host στο container: `COPY filename /dir/to/docker/container`
- Προεπιλογές για την εκτέλεση ενός container: `CMD command`
- Εκτέλεση εντολών μέσα στο container: `RUN command`
- Ποιες port κάνει expose το container: `EXPOSE 80/tcp`
- Κάνουμε set τον χρήστη: `USER username`
- Τρέχει όταν ξεκινήσει το container: `ENTRYPOINT [“executable”,”param1”,”param2”]`

SETUP Mongo Image
-
```
  docker pull mongo
  docker run -d -p 27017:27017 --name mongodb mongo
  docker start mongodb
  docker stop mongodb
```

COPY json data files 
-
```
  docker cp "MovieFlix2020_E17144_Stylianou_Ioannis\flask\data\movies.json" mongodb:/movies.json
  docker exec -it mongodb mongoimport --db=InfoSys --collection=Movies --drop --file=movies.json 
  docker cp "MovieFlix2020_E17144_Stylianou_Ioannis\flask\data\users.json" mongodb:/users.json
  docker exec -it mongodb mongoimport --db=InfoSys --collection=Users --drop --file=users.json 
```

VIEW Data in Mongodb Shell
-
```
  docker exec -it mongodb mongo
  db MovieFlix
  use MovieFlix
  show collections
  db.Movies.find()
  db.Users.find()
```

Mathematical Knowledge - Sum Recalculation
-

  https://math.stackexchange.com/questions/22348/how-to-add-and-subtract-values-from-an-average
  
  adding a value in sum of n:
  s' = s + (value -s) /n+1

  removing a value from sum of n:
  s' = (ns-value)/n-1

Στοιχεία επικοινωνίας
-
Στυλιανού Ιωάννης - jsm@hotmail.gr


# MovieFlix2020_E17144_Stylianou_Ioannis

<img src="https://i.imgur.com/tXbMaN0.png">

Απαλλακτική εργασία για το μάθημα Πληροφοριακά Συστήματα
### Υπεύθυνοι καθηγητές: 
- Χρυσόστομος Συμβουλίδης, simvoul@unipi.gr
- Jean-Didier Totow, totow@unipi.gr 

Python
-
#### Requirements - automatically install using requirements.txt
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
##### Την ip διεύθυνση του docker machine τη βρίσκουμε με την εντολη: `docker-machine ls` 

Συνδεόμαστε στο dockerized application τοποθετώντας τη διεύθυνση docker_machine_ip:5000, π.χ. 192.168.99.100:5000 ή localhost:5000
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

Εγκατάσταση mongodb image
-
```
  docker pull mongo
  docker run -d -p 27017:27017 --name mongodb mongo
  docker start mongodb
  docker stop mongodb
```

Αντιγραφή των αρχείων με τα data σε json
-
```
  docker cp "MovieFlix2020_E17144_Stylianou_Ioannis\flask\data\movies.json" mongodb:/movies.json
  docker exec -it mongodb mongoimport --db=InfoSys --collection=Movies --drop --file=movies.json 
  docker cp "MovieFlix2020_E17144_Stylianou_Ioannis\flask\data\users.json" mongodb:/users.json
  docker exec -it mongodb mongoimport --db=InfoSys --collection=Users --drop --file=users.json 
```

Προβολή δεδομένων σε MongoDB shell
-
```
  docker exec -it mongodb mongo
  db MovieFlix
  use MovieFlix
  show collections
  db.Movies.find()
  db.Users.find()
```
Επεξήγηση του Dockerfile
-
Επιλογή του base image για την νέα εικόνα που θα δημιουργήσουμε:

`FROM ubuntu:16.04 `

Όνομα και email του maintainer του image:

`MAINTAINER John St <e17144@unipi.gr - jsm@hotmail.gr>`

Εκτέλεση της εντολής apt-get update μέσα στο image:

`RUN apt-get update`

Εκτέλεση της εντολής μέσα στο image για την εγκατάσταση της python3 και του pip:

`RUN apt-get install -y python3 python3-pip `

Εκτέλεση της εντολής μέσα στο image για την εγκατάσταση των βασικών πακέτων στα οποία στηρίζεται το application μας. 

`RUN pip3 install flask pymongo `

Αντιγραφή του αρχείου requirements.txt από τον host στο directory /requirements:

`COPY requirements.txt /requirements/requirements.txt`

Εκτέλεση της εντολής εγκατάστασης των requirements από αρχείο μέσα στο image:

`RUN pip3 install -r requirements/requirements.txt`

Εκτέλεση της εντολής δημιουργίας φακέλου app στο image

`RUN mkdir /app`

Δημιουργία του directory /app/data και του /app εφόσον δεν υπάρχει (flag -p):

`RUN mkdir -p /app/data`

Αντιγραφή του service.py μέσα στο φάκελο app του image:

`COPY service.py /app/service.py`  

Αντιγραφή των html templates μέσα στο φάκελο templates:

`COPY templates /app/templates`

Αντιγραφή του data μέσα στο directory app/data:

`ADD data /app/data` 

Μετάβαση στο directory app :

`WORKDIR /app`

Ορισμός του default command που θα εκτελείται όταν τρέχει το container του image:

`ENTRYPOINT [ "python3","-u", "service.py" ]`

Composing with .yml 
-
Εκτελείτε την εντολή `docker-compose up` στο directory που βρίσκεται το αρχείο .yml

##### Για τελείως καθαρό build:
```
docker-compose rm --all &&
docker-compose pull &&
docker-compose build --no-cache &&
docker-compose up -d --force-recreate
```
Μετά την εκτέλεση της εντολής θα χρειαστεί να εισάγετε τα δεδομένα users.json, movies.json στα αντίστοιχα collection με τις εντολές στην ενότητα "Αντιγραφή των αρχείων με τα data σε json"

Μαθηματικές γνώσεις - Adjustment μέσου όρου χωρίς επανυπολογισμό
-

  https://math.stackexchange.com/questions/22348/how-to-add-and-subtract-values-from-an-average
  
  adding a value in sum of n:
  s' = s + (value-s) / n+1

  removing a value from sum of n:
  s' = s + (s-value) / (n-1)

![alt text](https://i.imgur.com/gCIAPRk.png)

Στοιχεία επικοινωνίας
-
Στυλιανού Ιωάννης - jsm@hotmail.gr


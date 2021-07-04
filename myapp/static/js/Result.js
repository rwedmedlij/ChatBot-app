const onMapData =
  "\n-----חריש-----1,880,000-----5-----5-----רובין 5-חריש-----050-9997483-----240-----https://www.onmap.co.il/home_details/ryDmNivhw-----מיזוג:מרוהט:יחידת הורים:משופצת:ממ״ד:מחסן:\n-----חריש-----1,020,000-----4-----4-----אתרוג 6-חריש-----050-9997483-----95-----https://www.onmap.co.il/home_details/H1OdC26cL-----יחידת הורים:ממ״ד:\n-----חריש-----1,040,000-----2-----4-----שוהם 4-חריש-----050-9997483-----120-----https://www.onmap.co.il/home_details/B1xNc3vkw-----מיזוג:יחידת הורים:משופצת:ממ״ד:מחסן:\n-----חריש-----965,000-----3-----3-----רימון-חריש-----050-9997483-----90-----https://www.onmap.co.il/home_details/HkAo56X5P-----מיזוג:משופצת:ממ״ד:מחסן:\n-----חריש-----1,140,000-----3-----5-----טורקיז 37-חריש-----050-8375471-----104-----https://www.onmap.co.il/home_details/rkzBa0vfP-----יחידת הורים:מחסן:";
const nadlanData =
  "1-----926,000-----חריש-----unknown-----3-----דרך ארץ-----80-----https://www.nadlan.com/property/1606741929559-----דוד שמש-----9 קומות בניין-----1 מעליות-----1 מרפסות-----2 חדרי שימוש-----גישה לנכים-----מחסן-----נכס   חזיתי, פינתי, עורפי-----מזגן:  הכנה למזגן מיני מרכזי-----חנייה:  אחת-----כיווני אוויר:   מערב, מזרח, דרום, צפון";

var all = onMapData.split("\n");
for (let i = 1; i < all.length; i++) {
  var str = all[i].split("-----");
  console.log(str);
  console.log("----------------------------------");
  var Bdiv = document.createElement("div");
  var img = document.createElement("img");
  var div = document.createElement("div");
  var h5 = document.createElement("h5");
  var p = document.createElement("p");
  var a = document.createElement("a");
  Bdiv.className = "card";
  Bdiv.style = "width: 18rem;";
  img.className = "card-img-top";
  div.className = "card-body";
  p.className = "card=text";
  h5.className = "card-title";
  h5.innerText = "at " + str[1];
  p.innerText =
    "the price is " +
    str[2] +
    " in floor number " +
    str[3] +
    " number of rooms is " +
    str[4] +
    " the address is " +
    str[5] +
    " phone number of the house Owner is " +
    str[6] +
    " the house is " +
    str[7] +
    " matters, some of addition in the house" +
    str[9];
  a.className = "btn btn-primary";
  a.innerText = "go to house";
  a.href = str[8];
  div.appendChild(h5);
  div.appendChild(p);
  div.appendChild(a);
  Bdiv.appendChild(img);
  Bdiv.appendChild(div);
  document.getElementById("result").appendChild(Bdiv);
}

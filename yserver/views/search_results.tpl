% include('header.tpl')
<div>
<br />
<div class="results">
<table>
  <tr>
% from bottle import request
   <td class="thead">R</td>
   <td class="thead">T</td>
   <td><a class="thead" href='?search={{request.query.search}}&sort=cat'>Categorie</a></td>
   <td><a class="thead" href='?search={{request.query.search}}&sort=title'>Titre</a></td>
   <td><a class="thead" href='?search={{request.query.search}}&sort=age'>Age</a></td>
   <td><a class="thead" href='?search={{request.query.search}}&sort=nsize'>Taille</a></td>
   <td><a class="thead" href='?search={{request.query.search}}&sort=seeders'>Seeders</a></td>
   <td><a class="thead" href='?search={{request.query.search}}&sort=leechers'>Leechers</a></td>
   <td class="thead">Lien</td>
  </tr>
%for r in results:
   <tr>
    <td><a href=/rt/{{r.tid}}>R</a></td>
    <td><a href=/ts/{{r.tid}}>T</a></td>
    <td>{{r.cat}}</td>
    <td><a class="torrent" href=/dl/{{r.tid}}>{{r.title}}</a></td>
    <td>{{r.age}}</td>
    <td>{{r.size}}</td>
    <td>{{r.seeders}}</td>
    <td>{{r.leechers}}</td>
    <td><a href='{{r.href}}'>X</a></td>
   </tr>
%end
 </table>
 </div>
</div>
% include('footer.tpl')

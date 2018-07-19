% include('header.tpl')
<div>
<br />
<div class="results">
<table>
  <tr>
% from bottle import request
   <td><a class="thead" href='?search={{request.query.search}}&sort=title'>Titre</a></td>
   <td><a class="thead" href='?search={{request.query.search}}&sort=age'>Age</a></td>
   <td><a class="thead" href='?search={{request.query.search}}&sort=size'>Taille</a></td>
   <td><a class="thead" href='?search={{request.query.search}}&sort=seeders'>Seeders</a></td>
   <td><a class="thead" href='?search={{request.query.search}}&sort=leechers'>Leechers</a></td>
  </tr>
%for r in results:
   <tr>
    <td><a class="torrent" href=/get/{{r.tid}}>{{r.title}}</a></td>
    <td>{{r.age}}</td>
    <td>{{r.size}}</td>
    <td>{{r.seeders}}</td>
    <td>{{r.leechers}}</td>
   </tr>
%end
 </table>
 </div>
</div>
% include('footer.tpl')

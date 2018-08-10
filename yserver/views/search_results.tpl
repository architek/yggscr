% include('header.tpl')
<div class="results">
<table>
  <tr>
% from bottle import request
%if state['rtEn']:
   <td class="thead">R</td>
%end
%if state['tsEn']:
   <td class="thead">T</td>
%end
%if state['dgEn']:
   <td class="thead">D</td>
%end
   <td><a class="thead" href='?search={{request.query.search}}&cat={{request.query.cat}}&subcat={{request.query.subcat}}&sort=cat'>Cat</a></td>
   <td><a class="thead" href='?search={{request.query.search}}&cat={{request.query.cat}}&subcat={{request.query.subcat}}&sort=subcat'>SubCat</a></td>
   <td><a class="thead" href='?search={{request.query.search}}&cat={{request.query.cat}}&subcat={{request.query.subcat}}&sort=title'>Titre</a></td>
   <td><a class="thead" href='?search={{request.query.search}}&cat={{request.query.cat}}&subcat={{request.query.subcat}}&sort=age'>Date</a></td>
   <td><a class="thead" href='?search={{request.query.search}}&cat={{request.query.cat}}&subcat={{request.query.subcat}}&sort=nsize'>Taille</a></td>
   <td><a class="thead" href='?search={{request.query.search}}&cat={{request.query.cat}}&subcat={{request.query.subcat}}&sort=seeders'>Seed</a></td>
   <td><a class="thead" href='?search={{request.query.search}}&cat={{request.query.cat}}&subcat={{request.query.subcat}}&sort=leechers'>Leech</a></td>
   <td class="thead">Lien</td>
  </tr>
%for r in state['sorted_torrents']:
   <tr>
%if state['rtEn']:
    <td><a href=/rt/{{r.tid}}>R</a></td>
%end
%if state['tsEn']:
    <td><a href=/ts/{{r.tid}}>T</a></td>
%end
%if state['dgEn']:
    <td><a href=/dg/{{r.tid}}>D</a></td>
%end
    <td>{{r.cat}}</td>
    <td>{{r.subcat}}</td>
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

% include('footer.tpl')

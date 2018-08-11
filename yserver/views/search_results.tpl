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
   <td class="thead">Cat</td>
   <td class="thead">SubCat</td>
   <td><a class="thead" href='{{state['qs']}}&sort=name'>Titre</a></td>
   <td><a class="thead" href='{{state['qs']}}&sort=publish_date'>Date</a></td>
   <td><a class="thead" href='{{state['qs']}}&sort=size'>Taille</a></td>
   <td><a class="thead" href='{{state['qs']}}&sort=seed'>Seed</a></td>
   <td><a class="thead" href='{{state['qs']}}&sort=seed'>Leech</a></td>
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
    <td>{{r.publish_date}}</td>
    <td>{{r.size}}</td>
    <td>{{r.seed}}</td>
    <td>{{r.leech}}</td>
    <td><a href='{{r.href}}'>X</a></td>
   </tr>
%end
 </table>
</div>

% include('footer.tpl')

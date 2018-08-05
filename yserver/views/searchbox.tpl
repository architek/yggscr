% from bottle import request
  <div class="searchbox">
  <form method="GET" action="/search">
  Texte
  <input type='text' name='name' id='name' value='{{request.query.name}}'/>
  Cat
  <input type='text' name='cat' id='cat' value='{{request.query.cat}}'/>
  SubCat
  <input type='text' name='subcat' id='subcat' value='{{request.query.subcat}}'/>
  Uploader
  <input type='text' name='uploader' id='uploader' value='{{request.query.uploader}}'/>
  <input type='submit' name="act" value='Rechercher' id='search'/>
  <input type='submit' name="act" value='Rssize' id='rssize'/>
  </form>
  </div>
%end


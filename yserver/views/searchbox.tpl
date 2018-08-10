% from bottle import request
  <div class="searchbox">
  <form method="GET" action="/search">
  Texte
  <input type='text' name='name' id='name' value='{{request.query.name}}'/>
  Cat
  <select id="cat" name="cat"></select>
  SubCat
  <select id="subcat" name="subcat"></select>
  Uploader
  <input type='text' name='uploader' id='uploader' value='{{request.query.uploader}}'/>
  <input type='submit' name="act" value='Rechercher' id='search'/>
  <input type='submit' name="act" value='Rssize' id='rssize'/>
  </form>
  </div>
%end


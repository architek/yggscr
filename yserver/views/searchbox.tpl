% from bottle import request
  <script type="text/javascript">
    var $CAT = "{{ request.query.category }}";
    var $SUBCAT = "{{ request.query.sub_category }}";
  </script>
  <div class="searchbox">
  <form action="/search">
  Texte
  <input type='text' name='name' id='name' value='{{request.query.name}}'/>
  Cat
  <select id="cat" name="category"></select>
  SubCat
  <select id="subcat" name="sub_category"></select>
  Uploader
  <input type='text' name='uploader' id='uploader' value='{{request.query.uploader}}'/>
  <input type='submit' name="act" value='Rechercher' id='search'/>
  <input type='submit' name="act" value='Rssize' id='rssize'/>
  </form>
  </div>
%end


function myFunction(lessonPlan) {
  var templateId = "1mJFVM8TiPce4kJ76P3NKuvn-NwRIZjYJzQt86rIRKJY";
  var doc = DocumentApp.openById(templateId);
  var body = doc.getBody();

  function escapeForReplaceText(str) {
    if (!str) return "";
    return str.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
  }

  ["Teacher","Year/Class","Subject","Unit/Topic","Week number","Date"].forEach(function(field){
    if (lessonPlan[field]) {
      body.replaceText("\\{\\{" + field + "\\}\\}", escapeForReplaceText(lessonPlan[field]));
    }
  });

  if (lessonPlan.Classes) {
    for (var classKey in lessonPlan.Classes) {
      var classObj = lessonPlan.Classes[classKey];
      for (var placeholder in classObj) {
        if (classObj[placeholder]) {
          body.replaceText("\\{\\{" + placeholder + "\\}\\}", escapeForReplaceText(classObj[placeholder]));
        }
      }
    }
  }

  doc.saveAndClose();
}

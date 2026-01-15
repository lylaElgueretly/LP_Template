function myFunction(lessonPlan) {
  // Open your Google Doc by ID
  var templateId = "1mJFVM8TiPce4kJ76P3NKuvn-NwRIZjYJzQt86rIRKJY";
  var doc = DocumentApp.openById(templateId);
  var body = doc.getBody();

  // Escape regex special characters for replaceText
  function escapeForReplaceText(str) {
    if (!str) return ""; // handle empty strings
    return str.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
  }

  // Replace top-level fields (headers) if present
  ["Teacher","Year/Class","Subject","Unit/Topic","Week number","Date"].forEach(function(field){
    if (lessonPlan[field]) {
      body.replaceText("\\{\\{" + field + "\\}\\}", escapeForReplaceText(lessonPlan[field]));
    }
  });

  // Replace all class placeholders
  if (lessonPlan.Classes) {
    for (var classKey in lessonPlan.Classes) {
      var classObj = lessonPlan.Classes[classKey];
      for (var placeholder in classObj) {
        if (classObj[placeholder]) {
          body.replaceText(
            "\\{\\{" + placeholder + "\\}\\}",
            escapeForReplaceText(classObj[placeholder])
          );
        }
      }
    }
  }

  // Save and close the document
  doc.saveAndClose();
}

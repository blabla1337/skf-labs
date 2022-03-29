package com.skf.labs.racecondition;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;

import org.springframework.core.io.InputStreamResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@Controller
public class RaceConditionController {
  @GetMapping("/{value}")
  public ResponseEntity<Object> downloadFile(@PathVariable String value, Model model) throws IOException {
    FileWriter fileWriter = new FileWriter("shared-file.txt", false);
    fileWriter.write(value);
    fileWriter.close();
    File file = new File("shared-file.txt");
    InputStreamResource resource = new InputStreamResource(new FileInputStream(file));
    HttpHeaders headers = new HttpHeaders();
    headers.add("Content-Disposition", String.format("attachment; filename=\"%s\"", file.getName()));
    headers.add("Cache-Control", "no-cache, no-store, must-revalidate");
    headers.add("Pragma", "no-cache");
    headers.add("Expires", "0");
    ResponseEntity<Object> responseEntity = ResponseEntity.ok().headers(headers).contentLength(file.length())
        .contentType(
            MediaType.parseMediaType("application/txt"))
        .body(resource);

    return responseEntity;
  }
}

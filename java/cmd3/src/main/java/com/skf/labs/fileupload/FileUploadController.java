package com.skf.labs.fileupload;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import com.skf.labs.fileupload.storage.StorageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

@Controller
public class FileUploadController {

  private final StorageService storageService;

  @Autowired
  public FileUploadController(StorageService storageService) {
    this.storageService = storageService;
  }

  @GetMapping("/")
  public String listUploadedFiles(Model modelAndView) throws IOException {
    modelAndView.addAttribute("systemCall", systemCall.getInstance());
    return "index";
  }

  @PostMapping("/")
  public String handleFileUpload(@RequestParam("file") MultipartFile file,
      Model model, Model modelAndView) throws IOException {
    if (allowedFile(file.getOriginalFilename())) {
      storageService.store(file);
      model.addAttribute("uploaded", "You successfully uploaded !");
    } else {
      model.addAttribute("uploaded", "File type not allowed");
    }
    modelAndView.addAttribute("systemCall", systemCall.getInstance());
    return "index";
  }

  public boolean allowedFile(String filename) {
    String[] allowedFileExtensions = new String[] { "txt", "pdf", "png", "jpg", "gif", "html" };
    String fileExtension = filename.substring(filename.lastIndexOf(".") + 1);
    if (java.util.Arrays.asList(allowedFileExtensions).contains(fileExtension)) {
      return true;
    } else {
      return false;
    }
  }

  private static class systemCall {
    private static systemCall instance = null;

    private systemCall() {
    }

    public static systemCall getInstance() {
      if (instance == null) {
        instance = new systemCall();
      }
      return instance;
    }

    public String utilityProcessor(String command) throws IOException {
      Process pb = new ProcessBuilder("/bin/sh", "-c",
          command)
          .redirectErrorStream(true)
          .start();
      BufferedReader br = new BufferedReader(new InputStreamReader(pb.getInputStream()));
      String line = "";
      StringBuilder sb = new StringBuilder();
      while ((line = br.readLine()) != null) {
        sb.append(line + "\n");
      }
      return sb.toString();
    }
  }

}
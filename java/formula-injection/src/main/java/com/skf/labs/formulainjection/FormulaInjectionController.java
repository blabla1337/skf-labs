package com.skf.labs.formulainjection;

import java.util.List;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.http.ResponseEntity;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.HttpStatus;
import java.io.IOException;
import java.io.ByteArrayOutputStream;
import org.apache.poi.xssf.usermodel.XSSFCell;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.CellStyle;
import org.apache.poi.ss.usermodel.DateUtil;
import org.apache.poi.ss.usermodel.FillPatternType;
import org.apache.poi.ss.usermodel.IndexedColors;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;




@Controller
public class FormulaInjectionController {
    @Autowired
    private FormulaInjectionModel formulaInjectionModel;


    @GetMapping("/")
    public String home(Model model) {
        List<Page> pages = formulaInjectionModel.getAllPages();
        model.addAttribute("menu", pages);
        return "index";
      }

    @GetMapping("/home/{id}")
    public String page(@PathVariable String id, Model model) {
        List<Page> pages = formulaInjectionModel.getAllPages();
        model.addAttribute("menu", pages);
        
        List<Page> page = formulaInjectionModel.getPage(id);
        model.addAttribute("page", page.get(0));
        return "index";
      }

      @PostMapping("/pages/add")
      public String addPage(@RequestParam(name="title", required=true) String title,@RequestParam(name="content", required=true) String content,Model model) {
          Page p = new Page(-1, title, content);

          if (formulaInjectionModel.addPage(p)){
            List<Page> pages = formulaInjectionModel.getAllPages();
            model.addAttribute("menu", pages);
            model.addAttribute("content", "Pages created sucessfully");
          }else{
            model.addAttribute("content", "Error on creating the page");
          }
          return "index";
        }

    @GetMapping("/pages/clear")
    public String clearPages(Model model) {
        if (formulaInjectionModel.clearPages()){
          List<Page> pages = formulaInjectionModel.getAllPages();
          model.addAttribute("menu", pages);
          model.addAttribute("content", "Pages cleared sucessfully");
        }else{
          model.addAttribute("content", "Error on clearing the pages");
        }
        return "index";
      }

      @GetMapping("/pages/export")
      public ResponseEntity<Resource>  exportPages(Model model) throws IOException {
        List<Page> pages = formulaInjectionModel.getAllPages();

        Workbook workbook = new XSSFWorkbook();
        Sheet sheet = workbook.createSheet("Pages");
        Row header = sheet.createRow(0);

        Cell headerCell = header.createCell(0);
        headerCell.setCellValue("Page ID");
        headerCell = header.createCell(1);
        headerCell.setCellValue("Title");
        headerCell = header.createCell(2);
        headerCell.setCellValue("Content");
       
        int xlsRow = 0;

        for(Page p : pages){
          Row row = sheet.createRow(xlsRow++);
          Cell cell = row.createCell(0);
          cell.setCellValue(p.getPageId());
          cell = row.createCell(1);
          cell.setCellValue(p.getTitle());
          cell = row.createCell(2);
          cell.setCellValue(p.getContent());
        }

        ByteArrayOutputStream ms = new ByteArrayOutputStream();
        workbook.write(ms);
        byte b[] = ms.toByteArray();

        ByteArrayResource resource = new ByteArrayResource(b);
        HttpHeaders httpHeader = new HttpHeaders();
        httpHeader.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=pages.xlsx");
        return ResponseEntity.ok().headers(httpHeader).contentLength(b.length).contentType(MediaType.parseMediaType("application/octet-stream")).body(resource);
      }
    
}

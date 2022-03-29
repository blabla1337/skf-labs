package com.skf.labs.xxe;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;

@Controller
public class XxeController {
	@PostMapping("/home")
	public String home(@RequestParam(name = "xxe", required = true, defaultValue = "xxe") String xxe, Model model) {
		// parse xxe xml and return nodes as string
		String nodes = "";
		try {
			DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
			DocumentBuilder builder = factory.newDocumentBuilder();
			InputStream is = new ByteArrayInputStream(xxe.getBytes());
			org.w3c.dom.Document doc = builder.parse(is);
			nodes = doc.getDocumentElement().getTextContent();
		} catch (ParserConfigurationException | IOException | org.xml.sax.SAXException e) {
			e.printStackTrace();
		}
		model.addAttribute("nodes", nodes);
		return "index";
	}
}
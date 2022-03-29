package com.skf.labs.graphqlidor.repository;
import com.skf.labs.graphqlidor.entity.Post;

import org.springframework.data.jpa.repository.JpaRepository;


public interface PostRepository extends JpaRepository<Post,Integer>{
    
}

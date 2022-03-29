package com.skf.labs.graphqlmutation.repository;
import com.skf.labs.graphqlmutation.entity.Post;

import org.springframework.data.jpa.repository.JpaRepository;


public interface PostRepository extends JpaRepository<Post,Integer>{
    
}

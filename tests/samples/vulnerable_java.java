import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.sql.ResultSet;

public class UserManager {
    public void getUser(String userId) {
        try {
            // Security: Hardcoded credentials
            Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/db", "root", "password123"); 
            Statement stmt = conn.createStatement();
            
            // Security: SQL Injection vulnerability
            String query = "SELECT * FROM users WHERE id = '" + userId + "'";
            ResultSet rs = stmt.executeQuery(query);
            
            while(rs.next()) {
                System.out.println(rs.getString("username"));
            }
        } catch (Exception e) {
            // Code Smell: Catching generic exception and not logging properly
            e.printStackTrace();
        }
    }
}
